# Commands

## FunC

```sh

func-js examples/foo.fc
func-js examples/foo2.fc

New-Item -ItemType Directory -Force examples/func | Out-Null; python -m universalmutator.genmutants examples/foo.fc func --only func.rules --mutantDir examples/func *> examples/func/check.out

New-Item -ItemType Directory -Force examples/func_all | Out-Null; python -m universalmutator.genmutants examples/foo.fc func --mutantDir examples/func_all *> examples/func_all/check.out

New-Item -ItemType Directory -Force examples/func2_all | Out-Null; python -m universalmutator.genmutants examples/foo2.fc func --mutantDir examples/func2_all *> examples/func2_all/check.out

# comby
mkdir examples/func2_all
python -m universalmutator.genmutants examples/foo2.fc func --mutantDir examples/func2_all --comby > examples/func2_all/check.out 2>&1
```

### Comby + compile-check (bash)

```sh
mkdir -p examples/func_comby_all
python -m universalmutator.genmutants examples/foo.fc func --mutantDir examples/func_comby_all --comby > examples/func_comby_all/check.out 2>&1

mkdir -p examples/func2_comby_all
python -m universalmutator.genmutants examples/foo2.fc func --mutantDir examples/func2_comby_all --comby > examples/func2_comby_all/check.out 2>&1
```

## Tact

```sh
New-Item -ItemType Directory -Force examples/tact | Out-Null; python -m universalmutator.genmutants examples/foo.tact tact --only tact.rules --mutantDir examples/tact *> examples/tact/check.out

New-Item -ItemType Directory -Force examples/tact_all | Out-Null; python -m universalmutator.genmutants examples/foo.tact tact --mutantDir examples/tact_all *> examples/tact_all/check.out

mkdir examples/tact_all
python -m universalmutator.genmutants examples/foo.tact tact --mutantDir examples/tact_all --comby > examples/tact_all/check.out 2>&1
```

### Comby + compile-check (bash)

```sh
mkdir -p examples/tact_comby
python -m universalmutator.genmutants examples/foo.tact tact --only tact.rules --mutantDir examples/tact_comby --comby > examples/tact_comby/check.out 2>&1

mkdir -p examples/tact_comby_all
python -m universalmutator.genmutants examples/foo.tact tact --mutantDir examples/tact_comby_all --comby > examples/tact_comby_all/check.out 2>&1
```

## Tolk

```sh
New-Item -ItemType Directory -Force examples/tolk | Out-Null; python -m universalmutator.genmutants examples/foo.tolk tolk --only tolk.rules --mutantDir examples/tolk *> examples/tolk/check.out

New-Item -ItemType Directory -Force examples/tolk_all | Out-Null; python -m universalmutator.genmutants examples/foo.tolk tolk --mutantDir examples/tolk_all *> examples/tolk_all/check.out

New-Item -ItemType Directory -Force examples/tolk2_all | Out-Null; python -m universalmutator.genmutants examples/foo2.tolk tolk --mutantDir examples/tolk2_all *> examples/tolk2_all/check.out
```

### Comby + compile-check (bash)

```sh
mkdir -p examples/tolk_comby_all
python -m universalmutator.genmutants examples/foo.tolk tolk --mutantDir examples/tolk_comby_all --comby > examples/tolk_comby_all/check.out 2>&1

mkdir -p examples/tolk2_comby_all
python -m universalmutator.genmutants examples/foo2.tolk tolk --mutantDir examples/tolk2_comby_all --comby > examples/tolk2_comby_all/check.out 2>&1
```

## Jetton (Tolk)

```sh
npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts

mutate examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk --mutantDir examples/tolk-jetton-wallet-mutants

analyze_mutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk "cd /d examples\tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" --mutantDir examples/tolk-jetton-wallet-mutants --timeout 180
```

## Jetton (FunC)

Перед запуском переключи wrapper на FunC:
`examples/tolk-bench/wrappers/01_jetton/JettonWallet.compile.ts`
должен быть с `lang: 'func'` и списком `targets` для `.fc` файлов.

```sh
npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts

mutate examples/tolk-bench/contracts_FunC/01_jetton/jetton-wallet.fc func --mutantDir examples/func-jetton-wallet-mutants

analyze_mutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-wallet.fc "cd /d examples\tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" --mutantDir examples/func-jetton-wallet-mutants --timeout 180
```

## Muton

```sh
muton run --test.cmd "npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" contracts_Tolk/01_jetton/jetton-wallet-contract.tolk
muton run contracts_Tolk/01_jetton/jetton-wallet-contract.tolk
```
