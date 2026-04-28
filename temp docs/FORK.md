# UniversalMutator + TON (Tact / FunC / Tolk)

This is a fork of `universalmutator` with support for three TON languages:

- `tact` for `.tact` files
- `func` for `.fc` and `.func` files
- `tolk` for `.tolk` files

## How to run this fork

The package already defines `console_scripts` in `setup.py`. After installing the fork, these commands are available:

- `mutate`
- `analyze_mutants`
- `check_covered`
- `prioritize_mutants`
- `show_mutants`
- `prune_mutants`
- `intersect_mutants`

### Option 1: editable install for development

This is the best setup if you actively modify the fork itself.

PowerShell:

```sh
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
python -m pip install -e . --no-build-isolation
mutate --help
```

What this gives you:

- the CLI is available immediately
- the current repository files are used directly
- no wheel rebuild is needed after code changes

If you do not need the CLI, you can run the module directly:

```sh
python -m universalmutator.genmutants --help
```

### Option 2: build a wheel and install it as a regular package

This is the setup for a full local CLI package.

PowerShell:

```sh
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel build
python -m build --wheel --no-isolation
python -m pip install --force-reinstall dist\*.whl
mutate --help
```

If `python -m build` prints `No module named build`, install it first:

```sh
python -m pip install build
```

For this fork, the wheel is built locally with:

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

## Installing TON compilers

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

## Mutant generation

The basic model is:

- `mutate` generates mutants
- for each mutant in `tact` / `tolk` / `func`, compile-check runs automatically through the language handler
- if the command returns `0`, the mutant is considered `VALID`
- `--cmd` is only needed if you want to force a custom validation command
- `--cmd` has priority over the built-in TON handlers and is useful for a custom compiler, wrapper, or local script
- in regex mode, multiline block comments `/* ... */`, `{- ... -}`, and empty lines are globally skipped for all languages

## Core changes (`mutator.py`)

- In regex mode, the mutator skips empty lines and block comments `/* ... */` and `{- ... -}` for all languages, to avoid mutating comments and inflating noise.
- For FunC, a fast regex-mode filter was added: if a line contains `store_uint` or `store_int` and also contains a long numeric sum expression (5+ numeric literals), numeric mutations from `universal.rules` of the form `(\D)(\d+)(\D)` are skipped. This speeds up generation and reduces the number of `INVALID` mutants on bit-width expressions. The filter is enabled only when `func.rules` is active and does not affect other languages or `--comby`.

### Generator changes (`genmutants.py`)

- With `--swap`, lines considered for swapping now exclude empty lines, comment lines (`//`, `;;`, `#`), and lines inside block comments `/* ... */` and `{- ... -}`. This makes swaps more meaningful and reduces noisy `INVALID` mutants.
- `--swap` also avoids swapping identical lines, including cases where `strip()` produces the same content, so it does not generate pointless mutants such as swapping `}` with `}`.

### 2026-04-28 update: mutator/comby sync

- `universalmutator/mutator.py`: import of `Comby` is now lazy inside `mutants_comby()`. Regular regex mutation flows and local tests no longer fail just because the Python `comby` package is missing.
- `universalmutator/mutator.py`: when `--comby` is used without the Python `comby` package, the tool now raises an explicit `ModuleNotFoundError` with a clear message instead of failing during top-level package import.

## 2026-04-28 core changes

- `universalmutator/mutator.py`: import of `Comby` is now lazy and happens only inside `mutants_comby()`. This removes the top-level hard dependency during module import, but does not replace the external `comby` binary requirement for actual `--comby` runs.
- `universalmutator/genmutants.py`: TON extensions `.tact`, `.fc`, `.func`, `.tolk` are mapped to Comby matcher `.generic` in `--comby` mode. Comby does not support TON-specific matcher names directly, so this avoids failures like `The matcher ".fc" is not supported`. Other languages keep their previous matcher behavior.

## Commands

### `mutate`

Generates mutants and writes them to `--mutantDir`. Add `--cmd` or `--noFastCheck` if needed.

```sh
mutate examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk --mutantDir tmp/tolk-jetton-wallet-mutants
```

### `analyze_mutants`

Runs tests against each mutant. Creates `killed.txt` and `notkilled.txt` in the current directory.

```sh
analyze_mutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk "cd /d examples\tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" --mutantDir tmp/tolk-jetton-wallet-mutants --timeout 180
```

Useful flags: `--show`, `--verbose`, `--resume`, `--noShuffle`, `--numMutants N`, `--prefix name`.

### `check_covered`

Filters mutants by covered lines. `coverfile` is a list of line numbers, one per line. For TSTL coverage reports, use `--tstl`.

```sh
check_covered examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk tmp/covered_lines.txt tmp/covered_mutants.txt --mutantDir tmp/tolk-jetton-wallet-mutants
```

### `prioritize_mutants`

Ranks a mutant list by structural distance. Input is a file containing mutant names.

```sh
prioritize_mutants tmp/covered_mutants.txt tmp/prioritized.txt --mutantDir tmp/tolk-jetton-wallet-mutants --sourceDir examples/tolk-bench/contracts_Tolk/01_jetton
```

### `show_mutants`

Shows diffs for mutants from a list.

```sh
show_mutants tmp/prioritized.txt --mutantDir tmp/tolk-jetton-wallet-mutants --sourceDir examples/tolk-bench/contracts_Tolk/01_jetton
```

The `--concise` flag makes the output more compact.

### `prune_mutants`

Filters a mutant list using a configuration file. Rule format is `field: value`; supported fields include `orig`, `mutant`, `change`, `source`, `line`, and their `!` / `_RE` variants.

```sh
prune_mutants tmp/prioritized.txt tmp/pruned.txt tmp/prune.cfg --mutantDir tmp/tolk-jetton-wallet-mutants --sourceDir examples/tolk-bench/contracts_Tolk/01_jetton
```

### `intersect_mutants`

Takes the intersection of two mutant lists.

```sh
intersect_mutants tmp/covered_mutants.txt tmp/prioritized.txt tmp/intersection.txt
```

For a smoke test, you can intersect any two existing lists, for example:

```sh
intersect_mutants tmp/all_mutants.txt tmp/prioritized.txt tmp/intersection.txt
```
