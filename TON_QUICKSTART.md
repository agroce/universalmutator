# UniversalMutator for TON: Quick Start

This file is a short practical guide for running `universalmutator` on TON projects.
The focus here is on real commands and a basic workflow:

## What is supported

- `Tolk` for `.tolk` -> `ton_common.rules + tolk.rules`
- `Tact` for `.tact` -> `ton_common.rules + tact.rules`
- `FunC` for `.fc` and `.func` -> `ton_common.rules + func.rules`

## Installation

### TON compilers

```bash
npm i -g @tact-lang/compiler
npm i -g @ton/tolk-js
npm i -g @ton-community/func-js
```

### Comby

If you need `--comby`:

```sh
python -m pip install comby
```

For `--comby`, you need not only the Python package but also an installed external `comby` binary.

## How to think about compile-check

There are two ways to specify your compile-check command:

- `--cmd "<command>"` for a single `mutate` run only
- `UM_TACT_CMD`, `UM_TOLK_CMD`, `UM_FUNC_CMD` as defaults for the current shell session

## Basic workflow

The minimal scenario is almost always this:

```sh
mutate <sourcefile> <tact|tolk|func> --mutantDir mutants

analyze_mutants <sourcefile> "<test command>" --mutantDir mutants --prefix run

show_mutants run.notkilled.txt --mutantDir mutants --sourceDir <source_dir> --concise
```

If there are many mutants, the next commands are:

- `prioritize_mutants`
- `prune_mutants`
- `intersect_mutants`

## Running in Acton

### Tolk in Acton

```sh
mutate contracts/src/Contract.tolk tolk --cmd "acton build"  --mutantDir mutants

analyze_mutants contracts/src/Contract.tolk "acton test" \
  --mutantDir mutants \
  --prefix tolk
```

## Running in Blueprint

### Tolk in Blueprint

```sh
mutate contracts/contract.tolk tolk --mutantDir mutants

analyze_mutants contracts/contract.tolk "npx blueprint test" \
  --mutantDir mutants \
  --prefix tolk

show_mutants tolk.notkilled.txt \
  --mutantDir mutants \
  --sourceDir contracts \
  --concise
```

### Tact in Blueprint

If the project is built through `build`, it is better to override the compile-check:

```sh
mutate contracts/contract.tact tact \
  --cmd "npx blueprint build --all" \
  --mutantDir mutants
```

If you need a full build and test run:

```sh
analyze_mutants contracts/contract.tact "npx blueprint test" \
  --mutantDir mutants \
  --prefix tact
```

### Real Tact example: `tact-lang/jetton`

```sh
git clone https://github.com/tact-lang/jetton
cd jetton
yarn

mutate src/contracts/base/jetton-minter.tact tact \
  --cmd "tact --config ./tact.config.json --project Jetton" \
  --mutantDir mutants
```

## Running for FunC

### Real FunC example: `tolk-bench`

```sh
git clone https://github.com/ton-blockchain/tolk-bench.git
cd tolk-bench
npm install

mutate contracts_FunC/01_jetton/jetton-minter-discoverable.fc func \
  --cmd 'npx func-js -C "contracts_FunC/01_jetton" params.fc op-codes.fc discovery-params.fc jetton-utils.fc jetton-minter-discoverable.fc' \
  --mutantDir mutants
```

If you are mutating not the entrypoint but an imported `.fc` file, this exact `--cmd` pattern is what you need: the build must go through the same target set the project actually uses.

## What to run after `analyze_mutants`

After `analyze_mutants`, you will usually get:

- `killed.txt` or `<prefix>.killed.txt`
- `notkilled.txt` or `<prefix>.notkilled.txt`

These files contain mutant names, and you can already use them with all post-processing commands.

### `show_mutants`

Shows exactly what changed in surviving mutants.

```sh
show_mutants func-minter.notkilled.txt \
  --mutantDir mutants \
  --sourceDir contracts_FunC/01_jetton \
  --concise
```

### `prioritize_mutants`

This command is useful if:

- there are too many surviving mutants
- tests are expensive
- you want to run the most diverse and informative mutations first

Basic example:

```sh
prioritize_mutants func-minter.notkilled.txt prioritized.txt 50 \
  --mutantDir mutants \
  --sourceDir contracts_FunC/01_jetton
```

What it does:

- takes the list of surviving mutants
- ranks them by difference
- keeps the top 50 in `prioritized.txt`

Then you can run:

```sh
show_mutants prioritized.txt \
  --mutantDir mutants \
  --sourceDir contracts_FunC/01_jetton \
  --concise
```

Or re-test only this subset:

```sh
analyze_mutants contracts_FunC/01_jetton/jetton-minter-discoverable.fc \
  "npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" \
  --mutantDir mutants \
  --fromFile prioritized.txt \
  --prefix prioritized-run
```
