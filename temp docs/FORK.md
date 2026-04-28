# UniversalMutator + TON (Tact / FunC / Tolk)

Это форк `universalmutator`, в который добавлена поддержка трех TON-языков:

- `tact` для файлов `.tact`
- `func` для файлов `.fc` и `.func`
- `tolk` для файлов `.tolk`

## Как запускать именно этот форк

У пакета уже есть `console_scripts` в `setup.py`. После установки форка доступны такие команды:

- `mutate`
- `analyze_mutants`
- `check_covered`
- `prioritize_mutants`
- `show_mutants`
- `prune_mutants`
- `intersect_mutants`

### Вариант 1: editable install для разработки

Это лучший режим, если ты активно правишь код форка.

PowerShell:

```sh
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
python -m pip install -e . --no-build-isolation
mutate --help
```

Что это дает:

- CLI появляется сразу
- используются текущие файлы из репозитория
- после правок не нужно пересобирать wheel

Если CLI не нужен, можно запускать напрямую модуль:

```sh
python -m universalmutator.genmutants --help
```

### Вариант 2: собрать wheel и поставить свою версию как обычный пакет

Это режим для полноценного локального CLI-пакета.

PowerShell:

```sh
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel build
python -m build --wheel --no-isolation
python -m pip install --force-reinstall dist\*.whl
mutate --help
```

Если `python -m build` пишет `No module named build`, сначала поставь:

```sh
python -m pip install build
```

Для этого форка wheel локально собирается командой:

```sh
python -m build --wheel --no-isolation
```

#### Bash

```sh
pip3 install tabulate
pip3 install comby

python -m build --wheel --no-isolation

python -m universalmutator.genmutants \
  examples/foo2.fc func \
  --mutantDir examples/func2_all \
  --comby \
  --noCheck \
  > examples/func2_all/check.out 2>&1

```

## Установка компиляторов TON

### Tact

```sh
npm i -g @tact-lang/compiler
tact --help
```

### Tolk

```sh
npm i -g @ton/tolk-js
tolk-js --help
```

### FunC

```sh
npm i -g @ton-community/func-js
func-js -h
```

## Генерация мутантов

Смысл такой:

- `mutate` генерирует мутантов
- для каждого мутанта для `tact` / `tolk` / `func` compile-check запускается автоматически через language handler
- если команда возвращает `0`, мутант считается `VALID`
- `--cmd` нужен только если хочется принудительно переопределить команду проверки
- `--cmd` имеет приоритет над встроенными TON handler-ами и подходит для нестандартного компилятора, обёртки или локального скрипта
- В regex-режиме многострочные блок-комментарии `/* ... */`, `{- ... -}` и пустые строки глобально пропускаются для всех языков

## Изменения ядра (mutator.py)

- В regex-режиме мутатор пропускает пустые строки и блок-комментарии `/* ... */` и `{- ... -}` для всех языков, чтобы не мутировать комментарии и не раздувать шум.
- Для FunC добавлен быстрый фильтр в regex-режиме: если строка содержит `store_uint` или `store_int` и выражение с длинной суммой чисел (5+ числовых литералов), то числовые мутации из `universal.rules` вида `(\D)(\d+)(\D)` пропускаются. Это ускоряет генерацию и уменьшает пачку `INVALID` на выражениях длины битов. Фильтр включается только при наличии `func.rules` и не влияет на другие языки или `--comby`.

### Изменения генератора (genmutants.py)

- При `--swap` строки для перестановки теперь исключают пустые строки и строки-комментарии (`//`, `;;`, `#`), а также строки внутри блок-комментариев `/* ... */` и `{- ... -}`. Это делает свапы более осмысленными и уменьшает число мусорных `INVALID`.
- Также `--swap` не переставляет одинаковые строки (включая случаи, когда совпадает содержимое после `strip()`), чтобы не генерировать бессмысленные мутанты вроде перестановки `}` с `}`.

### 2026-04-28 update: mutator/comby sync

- `universalmutator/mutator.py`: import of `Comby` is now lazy inside `mutants_comby()`. Regular regex mutation flows and local tests no longer fail just because the Python `comby` package is missing.
- `universalmutator/mutator.py`: when `--comby` is used without the Python `comby` package, the tool now raises an explicit `ModuleNotFoundError` with a clear message instead of failing during top-level package import.

## 2026-04-28 core changes

- `universalmutator/mutator.py`: import of `Comby` is now lazy and happens only inside `mutants_comby()`. This removes the top-level hard dependency during module import, but does not replace the external `comby` binary requirement for actual `--comby` runs.
- `universalmutator/genmutants.py`: TON extensions `.tact`, `.fc`, `.func`, `.tolk` are mapped to Comby matcher `.generic` in `--comby` mode. Comby does not support TON-specific matcher names directly, so this avoids failures like `The matcher ".fc" is not supported`. Other languages keep their previous matcher behavior.

## Команды

### `mutate`

Генерирует мутантов и кладёт их в `--mutantDir`. При необходимости можно добавить `--cmd` или `--noFastCheck`.

```sh
mutate examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk --mutantDir tmp/tolk-jetton-wallet-mutants
```

### `analyze_mutants`

Прогоняет тесты на каждом мутанте. Создаёт `killed.txt` и `notkilled.txt` в текущей директории.

```sh
analyze_mutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk "cd /d examples\tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" --mutantDir tmp/tolk-jetton-wallet-mutants --timeout 180
```

Полезные флаги: `--show`, `--verbose`, `--resume`, `--noShuffle`, `--numMutants N`, `--prefix name`.

### `check_covered`

Фильтрует мутантов по покрытым строкам. Формат `coverfile` — список номеров строк (по одному номеру на строку). Для TSTL-отчётов есть `--tstl`.

```sh
check_covered examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk tmp/covered_lines.txt tmp/covered_mutants.txt --mutantDir tmp/tolk-jetton-wallet-mutants
```

### `prioritize_mutants`

Ранжирует список мутантов по структурной дистанции. На вход принимает файл со списком имён мутантов.

```sh
prioritize_mutants tmp/covered_mutants.txt tmp/prioritized.txt --mutantDir tmp/tolk-jetton-wallet-mutants --sourceDir examples/tolk-bench/contracts_Tolk/01_jetton
```

### `show_mutants`

Показывает диффы для мутантов из списка.

```sh
show_mutants tmp/prioritized.txt --mutantDir tmp/tolk-jetton-wallet-mutants --sourceDir examples/tolk-bench/contracts_Tolk/01_jetton
```

Флаг `--concise` делает вывод компактным.

### `prune_mutants`

Фильтрует список мутантов по правилам из конфигурации. Формат правил — строки вида `field: value`, доступны `orig`, `mutant`, `change`, `source`, `line` и их варианты с `!` или `_RE`.

```sh
prune_mutants tmp/prioritized.txt tmp/pruned.txt tmp/prune.cfg --mutantDir tmp/tolk-jetton-wallet-mutants --sourceDir examples/tolk-bench/contracts_Tolk/01_jetton
```

### `intersect_mutants`

Берёт пересечение двух списков мутантов.

```sh
intersect_mutants tmp/covered_mutants.txt tmp/prioritized.txt tmp/intersection.txt
```

Для smoke-теста можно пересекать любые два существующих списка, например:

```sh
intersect_mutants tmp/all_mutants.txt tmp/prioritized.txt tmp/intersection.txt
```
