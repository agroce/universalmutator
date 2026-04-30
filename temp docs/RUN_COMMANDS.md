# Mutant Generation & Analysis Commands (Linux)

## Tolk

### 01 Jetton

```bash
# --- jetton-minter-contract.tolk ---
mkdir -p tmp/tolk-bench/01_jetton/tolk-minter-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-minter-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/01_jetton/tolk-minter-only > tmp/tolk-bench/01_jetton/tolk-minter-only/check.out 2>&1

mkdir -p tmp/tolk-bench/01_jetton/tolk-minter-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-minter-contract.tolk tolk --mutantDir tmp/tolk-bench/01_jetton/tolk-minter-all > tmp/tolk-bench/01_jetton/tolk-minter-all/check.out 2>&1

mkdir -p tmp/tolk-bench/01_jetton/tolk-minter-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-minter-contract.tolk tolk --mutantDir tmp/tolk-bench/01_jetton/tolk-minter-comby --comby > tmp/tolk-bench/01_jetton/tolk-minter-comby/check.out 2>&1

# --- jetton-wallet-contract.tolk ---
mkdir -p tmp/tolk-bench/01_jetton/tolk-wallet-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/01_jetton/tolk-wallet-only > tmp/tolk-bench/01_jetton/tolk-wallet-only/check.out 2>&1

mkdir -p tmp/tolk-bench/01_jetton/tolk-wallet-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk tolk --mutantDir tmp/tolk-bench/01_jetton/tolk-wallet-all > tmp/tolk-bench/01_jetton/tolk-wallet-all/check.out 2>&1

mkdir -p tmp/tolk-bench/01_jetton/tolk-wallet-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk tolk --mutantDir tmp/tolk-bench/01_jetton/tolk-wallet-comby --comby > tmp/tolk-bench/01_jetton/tolk-wallet-comby/check.out 2>&1

# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/01_jetton/tolk-wallet-all \
  --timeout 300 > tmp/tolk-bench/01_jetton/tolk-wallet-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-wallet-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/01_jetton/tolk-wallet-comby \
  --timeout 300 > tmp/tolk-bench/01_jetton/tolk-wallet-comby/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-minter-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/01_jetton/tolk-minter-all \
  --timeout 300 > tmp/tolk-bench/01_jetton/tolk-minter-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/01_jetton/jetton-minter-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/01_jetton/tolk-minter-comby \
  --timeout 300 > tmp/tolk-bench/01_jetton/tolk-minter-comby/analyze.out 2>&1
```

### 02 NFT

```bash
# --- nft-collection-contract.tolk ---
mkdir -p tmp/tolk-bench/02_nft/tolk-collection-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/02_nft/nft-collection-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/02_nft/tolk-collection-only > tmp/tolk-bench/02_nft/tolk-collection-only/check.out 2>&1

mkdir -p tmp/tolk-bench/02_nft/tolk-collection-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/02_nft/nft-collection-contract.tolk tolk --mutantDir tmp/tolk-bench/02_nft/tolk-collection-all > tmp/tolk-bench/02_nft/tolk-collection-all/check.out 2>&1

mkdir -p tmp/tolk-bench/02_nft/tolk-collection-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/02_nft/nft-collection-contract.tolk tolk --mutantDir tmp/tolk-bench/02_nft/tolk-collection-comby --comby > tmp/tolk-bench/02_nft/tolk-collection-comby/check.out 2>&1

# --- nft-item-contract.tolk ---
mkdir -p tmp/tolk-bench/02_nft/tolk-item-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/02_nft/nft-item-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/02_nft/tolk-item-only > tmp/tolk-bench/02_nft/tolk-item-only/check.out 2>&1

mkdir -p tmp/tolk-bench/02_nft/tolk-item-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/02_nft/nft-item-contract.tolk tolk --mutantDir tmp/tolk-bench/02_nft/tolk-item-all > tmp/tolk-bench/02_nft/tolk-item-all/check.out 2>&1

mkdir -p tmp/tolk-bench/02_nft/tolk-item-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/02_nft/nft-item-contract.tolk tolk --mutantDir tmp/tolk-bench/02_nft/tolk-item-comby --comby > tmp/tolk-bench/02_nft/tolk-item-comby/check.out 2>&1

# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_Tolk/02_nft/nft-collection-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/02_nft/NFTCollectionAndItem.spec.ts" \
  --mutantDir tmp/tolk-bench/02_nft/tolk-collection-all \
  --timeout 300 > tmp/tolk-bench/02_nft/tolk-collection-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/02_nft/nft-collection-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/02_nft/NFTCollectionAndItem.spec.ts" \
  --mutantDir tmp/tolk-bench/02_nft/tolk-collection-comby \
  --timeout 300 > tmp/tolk-bench/02_nft/tolk-collection-comby/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/02_nft/nft-item-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/02_nft/NFTCollectionAndItem.spec.ts" \
  --mutantDir tmp/tolk-bench/02_nft/tolk-item-all \
  --timeout 300 > tmp/tolk-bench/02_nft/tolk-item-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/02_nft/nft-item-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/02_nft/NFTCollectionAndItem.spec.ts" \
  --mutantDir tmp/tolk-bench/02_nft/tolk-item-comby \
  --timeout 300 > tmp/tolk-bench/02_nft/tolk-item-comby/analyze.out 2>&1
```

### 03 Notcoin

```bash
# --- jetton-minter-contract.tolk ---
mkdir -p tmp/tolk-bench/03_notcoin/tolk-minter-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/03_notcoin/jetton-minter-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/03_notcoin/tolk-minter-only > tmp/tolk-bench/03_notcoin/tolk-minter-only/check.out 2>&1

mkdir -p tmp/tolk-bench/03_notcoin/tolk-minter-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/03_notcoin/jetton-minter-contract.tolk tolk --mutantDir tmp/tolk-bench/03_notcoin/tolk-minter-all > tmp/tolk-bench/03_notcoin/tolk-minter-all/check.out 2>&1

mkdir -p tmp/tolk-bench/03_notcoin/tolk-minter-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/03_notcoin/jetton-minter-contract.tolk tolk --mutantDir tmp/tolk-bench/03_notcoin/tolk-minter-comby --comby > tmp/tolk-bench/03_notcoin/tolk-minter-comby/check.out 2>&1

# --- jetton-wallet-contract.tolk ---
mkdir -p tmp/tolk-bench/03_notcoin/tolk-wallet-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/03_notcoin/jetton-wallet-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/03_notcoin/tolk-wallet-only > tmp/tolk-bench/03_notcoin/tolk-wallet-only/check.out 2>&1

mkdir -p tmp/tolk-bench/03_notcoin/tolk-wallet-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/03_notcoin/jetton-wallet-contract.tolk tolk --mutantDir tmp/tolk-bench/03_notcoin/tolk-wallet-all > tmp/tolk-bench/03_notcoin/tolk-wallet-all/check.out 2>&1

mkdir -p tmp/tolk-bench/03_notcoin/tolk-wallet-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/03_notcoin/jetton-wallet-contract.tolk tolk --mutantDir tmp/tolk-bench/03_notcoin/tolk-wallet-comby --comby > tmp/tolk-bench/03_notcoin/tolk-wallet-comby/check.out 2>&1

# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_Tolk/03_notcoin/jetton-wallet-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/03_notcoin/Notcoin.spec.ts" \
  --mutantDir tmp/tolk-bench/03_notcoin/tolk-wallet-all \
  --timeout 300 > tmp/tolk-bench/03_notcoin/tolk-wallet-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/03_notcoin/jetton-wallet-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/03_notcoin/Notcoin.spec.ts" \
  --mutantDir tmp/tolk-bench/03_notcoin/tolk-wallet-comby \
  --timeout 300 > tmp/tolk-bench/03_notcoin/tolk-wallet-comby/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/03_notcoin/jetton-minter-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/03_notcoin/Notcoin.spec.ts" \
  --mutantDir tmp/tolk-bench/03_notcoin/tolk-minter-all \
  --timeout 300 > tmp/tolk-bench/03_notcoin/tolk-minter-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/03_notcoin/jetton-minter-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/03_notcoin/Notcoin.spec.ts" \
  --mutantDir tmp/tolk-bench/03_notcoin/tolk-minter-comby \
  --timeout 300 > tmp/tolk-bench/03_notcoin/tolk-minter-comby/analyze.out 2>&1
```

### 04 Sharded TgBTC

```bash
# --- jetton-wallet-contract.tolk ---
mkdir -p tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/04_sharded_tgbtc/jetton-wallet-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-only > tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-only/check.out 2>&1

mkdir -p tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/04_sharded_tgbtc/jetton-wallet-contract.tolk tolk --mutantDir tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-all > tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-all/check.out 2>&1

mkdir -p tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/04_sharded_tgbtc/jetton-wallet-contract.tolk tolk --mutantDir tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-comby --comby > tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-comby/check.out 2>&1

# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_Tolk/04_sharded_tgbtc/jetton-wallet-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/04_sharded_tgbtc/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-all \
  --timeout 300 > tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/04_sharded_tgbtc/jetton-wallet-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/04_sharded_tgbtc/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-comby \
  --timeout 300 > tmp/tolk-bench/04_sharded_tgbtc/tolk-wallet-comby/analyze.out 2>&1
```

### 05 Wallet V5

```bash
# --- wallet-v5-contract.tolk ---
mkdir -p tmp/tolk-bench/05_wallet-v5/tolk-wallet-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/05_wallet-v5/wallet-v5-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/05_wallet-v5/tolk-wallet-only > tmp/tolk-bench/05_wallet-v5/tolk-wallet-only/check.out 2>&1

mkdir -p tmp/tolk-bench/05_wallet-v5/tolk-wallet-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/05_wallet-v5/wallet-v5-contract.tolk tolk --mutantDir tmp/tolk-bench/05_wallet-v5/tolk-wallet-all > tmp/tolk-bench/05_wallet-v5/tolk-wallet-all/check.out 2>&1

mkdir -p tmp/tolk-bench/05_wallet-v5/tolk-wallet-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/05_wallet-v5/wallet-v5-contract.tolk tolk --mutantDir tmp/tolk-bench/05_wallet-v5/tolk-wallet-comby --comby > tmp/tolk-bench/05_wallet-v5/tolk-wallet-comby/check.out 2>&1

# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_Tolk/05_wallet-v5/wallet-v5-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/05_wallet-v5/WalletW5.spec.ts" \
  --mutantDir tmp/tolk-bench/05_wallet-v5/tolk-wallet-all \
  --timeout 300 > tmp/tolk-bench/05_wallet-v5/tolk-wallet-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/05_wallet-v5/wallet-v5-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/05_wallet-v5/WalletW5.spec.ts" \
  --mutantDir tmp/tolk-bench/05_wallet-v5/tolk-wallet-comby \
  --timeout 300 > tmp/tolk-bench/05_wallet-v5/tolk-wallet-comby/analyze.out 2>&1
```

### 06 Vesting

```bash
# --- vesting-contract.tolk ---
mkdir -p tmp/tolk-bench/06_vesting/tolk-vesting-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/06_vesting/vesting-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/06_vesting/tolk-vesting-only > tmp/tolk-bench/06_vesting/tolk-vesting-only/check.out 2>&1

mkdir -p tmp/tolk-bench/06_vesting/tolk-vesting-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/06_vesting/vesting-contract.tolk tolk --mutantDir tmp/tolk-bench/06_vesting/tolk-vesting-all > tmp/tolk-bench/06_vesting/tolk-vesting-all/check.out 2>&1

mkdir -p tmp/tolk-bench/06_vesting/tolk-vesting-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/06_vesting/vesting-contract.tolk tolk --mutantDir tmp/tolk-bench/06_vesting/tolk-vesting-comby --comby > tmp/tolk-bench/06_vesting/tolk-vesting-comby/check.out 2>&1

# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_Tolk/06_vesting/vesting-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/06_vesting/VestingWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/06_vesting/tolk-vesting-all \
  --timeout 300 > tmp/tolk-bench/06_vesting/tolk-vesting-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/06_vesting/vesting-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/06_vesting/VestingWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/06_vesting/tolk-vesting-comby \
  --timeout 300 > tmp/tolk-bench/06_vesting/tolk-vesting-comby/analyze.out 2>&1
```

### 07 Telemint

```bash
# --- telemint-collection-contract.tolk ---
mkdir -p tmp/tolk-bench/07_telemint/tolk-collection-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/07_telemint/telemint-collection-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/07_telemint/tolk-collection-only > tmp/tolk-bench/07_telemint/tolk-collection-only/check.out 2>&1

mkdir -p tmp/tolk-bench/07_telemint/tolk-collection-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/07_telemint/telemint-collection-contract.tolk tolk --mutantDir tmp/tolk-bench/07_telemint/tolk-collection-all > tmp/tolk-bench/07_telemint/tolk-collection-all/check.out 2>&1

mkdir -p tmp/tolk-bench/07_telemint/tolk-collection-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/07_telemint/telemint-collection-contract.tolk tolk --mutantDir tmp/tolk-bench/07_telemint/tolk-collection-comby --comby > tmp/tolk-bench/07_telemint/tolk-collection-comby/check.out 2>&1

# --- telemint-item-contract.tolk ---
mkdir -p tmp/tolk-bench/07_telemint/tolk-item-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/07_telemint/telemint-item-contract.tolk tolk --only tolk.rules --mutantDir tmp/tolk-bench/07_telemint/tolk-item-only > tmp/tolk-bench/07_telemint/tolk-item-only/check.out 2>&1

mkdir -p tmp/tolk-bench/07_telemint/tolk-item-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/07_telemint/telemint-item-contract.tolk tolk --mutantDir tmp/tolk-bench/07_telemint/tolk-item-all > tmp/tolk-bench/07_telemint/tolk-item-all/check.out 2>&1

mkdir -p tmp/tolk-bench/07_telemint/tolk-item-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_Tolk/07_telemint/telemint-item-contract.tolk tolk --mutantDir tmp/tolk-bench/07_telemint/tolk-item-comby --comby > tmp/tolk-bench/07_telemint/tolk-item-comby/check.out 2>&1

# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_Tolk/07_telemint/telemint-collection-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/07_telemint/Nft.spec.ts" \
  --mutantDir tmp/tolk-bench/07_telemint/tolk-collection-all \
  --timeout 300 > tmp/tolk-bench/07_telemint/tolk-collection-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/07_telemint/telemint-collection-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/07_telemint/Nft.spec.ts" \
  --mutantDir tmp/tolk-bench/07_telemint/tolk-collection-comby \
  --timeout 300 > tmp/tolk-bench/07_telemint/tolk-collection-comby/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/07_telemint/telemint-item-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/07_telemint/Nft.spec.ts" \
  --mutantDir tmp/tolk-bench/07_telemint/tolk-item-all \
  --timeout 300 > tmp/tolk-bench/07_telemint/tolk-item-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_Tolk/07_telemint/telemint-item-contract.tolk \
  "cd examples/tolk-bench && npx jest --runInBand tests/07_telemint/Nft.spec.ts" \
  --mutantDir tmp/tolk-bench/07_telemint/tolk-item-comby \
  --timeout 300 > tmp/tolk-bench/07_telemint/tolk-item-comby/analyze.out 2>&1
```

---

## FunC

> Before running `analyze_mutants` for FunC versions, switch the wrapper to `lang: 'func'` and the correct `targets` list for `.fc` files in the corresponding `.compile.ts` file.

### 01 Jetton

```bash
# --- jetton-minter-discoverable.fc ---
mkdir -p tmp/tolk-bench/01_jetton/func-minter-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-minter-discoverable.fc func --only func.rules --mutantDir tmp/tolk-bench/01_jetton/func-minter-only > tmp/tolk-bench/01_jetton/func-minter-only/check.out 2>&1

mkdir -p tmp/tolk-bench/01_jetton/func-minter-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-minter-discoverable.fc func --mutantDir tmp/tolk-bench/01_jetton/func-minter-all > tmp/tolk-bench/01_jetton/func-minter-all/check.out 2>&1

mkdir -p tmp/tolk-bench/01_jetton/func-minter-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-minter-discoverable.fc func --mutantDir tmp/tolk-bench/01_jetton/func-minter-comby --comby > tmp/tolk-bench/01_jetton/func-minter-comby/check.out 2>&1

# --- jetton-wallet.fc ---
mkdir -p tmp/tolk-bench/01_jetton/func-wallet-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-wallet.fc func --only func.rules --mutantDir tmp/tolk-bench/01_jetton/func-wallet-only > tmp/tolk-bench/01_jetton/func-wallet-only/check.out 2>&1

mkdir -p tmp/tolk-bench/01_jetton/func-wallet-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-wallet.fc func --mutantDir tmp/tolk-bench/01_jetton/func-wallet-all > tmp/tolk-bench/01_jetton/func-wallet-all/check.out 2>&1

mkdir -p tmp/tolk-bench/01_jetton/func-wallet-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-wallet.fc func --mutantDir tmp/tolk-bench/01_jetton/func-wallet-comby --comby > tmp/tolk-bench/01_jetton/func-wallet-comby/check.out 2>&1
```

```sh
# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-wallet.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/01_jetton/func-wallet-all \
  --timeout 300 > tmp/tolk-bench/01_jetton/func-wallet-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-wallet.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/01_jetton/func-wallet-comby \
  --timeout 300 > tmp/tolk-bench/01_jetton/func-wallet-comby/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-minter-discoverable.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/01_jetton/func-minter-all \
  --timeout 300 > tmp/tolk-bench/01_jetton/func-minter-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/01_jetton/jetton-minter-discoverable.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/01_jetton/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/01_jetton/func-minter-comby \
  --timeout 300 > tmp/tolk-bench/01_jetton/func-minter-comby/analyze.out 2>&1
```

### 02 NFT

```bash
# --- nft-collection.fc ---
mkdir -p tmp/tolk-bench/02_nft/func-collection-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/02_nft/nft-collection.fc func --only func.rules --mutantDir tmp/tolk-bench/02_nft/func-collection-only > tmp/tolk-bench/02_nft/func-collection-only/check.out 2>&1

mkdir -p tmp/tolk-bench/02_nft/func-collection-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/02_nft/nft-collection.fc func --mutantDir tmp/tolk-bench/02_nft/func-collection-all > tmp/tolk-bench/02_nft/func-collection-all/check.out 2>&1

mkdir -p tmp/tolk-bench/02_nft/func-collection-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/02_nft/nft-collection.fc func --mutantDir tmp/tolk-bench/02_nft/func-collection-comby --comby > tmp/tolk-bench/02_nft/func-collection-comby/check.out 2>&1

# --- nft-item.fc ---
mkdir -p tmp/tolk-bench/02_nft/func-item-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/02_nft/nft-item.fc func --only func.rules --mutantDir tmp/tolk-bench/02_nft/func-item-only > tmp/tolk-bench/02_nft/func-item-only/check.out 2>&1

mkdir -p tmp/tolk-bench/02_nft/func-item-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/02_nft/nft-item.fc func --mutantDir tmp/tolk-bench/02_nft/func-item-all > tmp/tolk-bench/02_nft/func-item-all/check.out 2>&1

mkdir -p tmp/tolk-bench/02_nft/func-item-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/02_nft/nft-item.fc func --mutantDir tmp/tolk-bench/02_nft/func-item-comby --comby > tmp/tolk-bench/02_nft/func-item-comby/check.out 2>&1
```

```sh
# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_FunC/02_nft/nft-collection.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/02_nft/NFTCollectionAndItem.spec.ts" \
  --mutantDir tmp/tolk-bench/02_nft/func-collection-all \
  --timeout 300 > tmp/tolk-bench/02_nft/func-collection-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/02_nft/nft-collection.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/02_nft/NFTCollectionAndItem.spec.ts" \
  --mutantDir tmp/tolk-bench/02_nft/func-collection-comby \
  --timeout 300 > tmp/tolk-bench/02_nft/func-collection-comby/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/02_nft/nft-item.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/02_nft/NFTCollectionAndItem.spec.ts" \
  --mutantDir tmp/tolk-bench/02_nft/func-item-all \
  --timeout 300 > tmp/tolk-bench/02_nft/func-item-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/02_nft/nft-item.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/02_nft/NFTCollectionAndItem.spec.ts" \
  --mutantDir tmp/tolk-bench/02_nft/func-item-comby \
  --timeout 300 > tmp/tolk-bench/02_nft/func-item-comby/analyze.out 2>&1
```

### 03 Notcoin

```bash
# --- jetton-minter-not.fc ---
mkdir -p tmp/tolk-bench/03_notcoin/func-minter-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/03_notcoin/jetton-minter-not.fc func --only func.rules --mutantDir tmp/tolk-bench/03_notcoin/func-minter-only > tmp/tolk-bench/03_notcoin/func-minter-only/check.out 2>&1

mkdir -p tmp/tolk-bench/03_notcoin/func-minter-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/03_notcoin/jetton-minter-not.fc func --mutantDir tmp/tolk-bench/03_notcoin/func-minter-all > tmp/tolk-bench/03_notcoin/func-minter-all/check.out 2>&1

mkdir -p tmp/tolk-bench/03_notcoin/func-minter-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/03_notcoin/jetton-minter-not.fc func --mutantDir tmp/tolk-bench/03_notcoin/func-minter-comby --comby > tmp/tolk-bench/03_notcoin/func-minter-comby/check.out 2>&1

# --- jetton-wallet-not.fc ---
mkdir -p tmp/tolk-bench/03_notcoin/func-wallet-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/03_notcoin/jetton-wallet-not.fc func --only func.rules --mutantDir tmp/tolk-bench/03_notcoin/func-wallet-only > tmp/tolk-bench/03_notcoin/func-wallet-only/check.out 2>&1

mkdir -p tmp/tolk-bench/03_notcoin/func-wallet-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/03_notcoin/jetton-wallet-not.fc func --mutantDir tmp/tolk-bench/03_notcoin/func-wallet-all > tmp/tolk-bench/03_notcoin/func-wallet-all/check.out 2>&1

mkdir -p tmp/tolk-bench/03_notcoin/func-wallet-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/03_notcoin/jetton-wallet-not.fc func --mutantDir tmp/tolk-bench/03_notcoin/func-wallet-comby --comby > tmp/tolk-bench/03_notcoin/func-wallet-comby/check.out 2>&1
```

```sh
# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_FunC/03_notcoin/jetton-minter-not.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/03_notcoin/Notcoin.spec.ts" \
  --mutantDir tmp/tolk-bench/03_notcoin/func-minter-all \
  --timeout 300 > tmp/tolk-bench/03_notcoin/func-minter-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/03_notcoin/jetton-minter-not.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/03_notcoin/Notcoin.spec.ts" \
  --mutantDir tmp/tolk-bench/03_notcoin/func-minter-comby \
  --timeout 300 > tmp/tolk-bench/03_notcoin/func-minter-comby/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/03_notcoin/jetton-wallet-not.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/03_notcoin/Notcoin.spec.ts" \
  --mutantDir tmp/tolk-bench/03_notcoin/func-wallet-all \
  --timeout 300 > tmp/tolk-bench/03_notcoin/func-wallet-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/03_notcoin/jetton-wallet-not.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/03_notcoin/Notcoin.spec.ts" \
  --mutantDir tmp/tolk-bench/03_notcoin/func-wallet-comby \
  --timeout 300 > tmp/tolk-bench/03_notcoin/func-wallet-comby/analyze.out 2>&1
```

### 04 Sharded TgBTC

```bash
# --- jetton-wallet.fc ---
mkdir -p tmp/tolk-bench/04_sharded_tgbtc/func-wallet-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/04_sharded_tgbtc/jetton-wallet.fc func --only func.rules --mutantDir tmp/tolk-bench/04_sharded_tgbtc/func-wallet-only > tmp/tolk-bench/04_sharded_tgbtc/func-wallet-only/check.out 2>&1

mkdir -p tmp/tolk-bench/04_sharded_tgbtc/func-wallet-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/04_sharded_tgbtc/jetton-wallet.fc func --mutantDir tmp/tolk-bench/04_sharded_tgbtc/func-wallet-all > tmp/tolk-bench/04_sharded_tgbtc/func-wallet-all/check.out 2>&1

mkdir -p tmp/tolk-bench/04_sharded_tgbtc/func-wallet-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/04_sharded_tgbtc/jetton-wallet.fc func --mutantDir tmp/tolk-bench/04_sharded_tgbtc/func-wallet-comby --comby > tmp/tolk-bench/04_sharded_tgbtc/func-wallet-comby/check.out 2>&1
```

```sh
# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_FunC/04_sharded_tgbtc/jetton-wallet.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/04_sharded_tgbtc/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/04_sharded_tgbtc/func-wallet-all \
  --timeout 300 > tmp/tolk-bench/04_sharded_tgbtc/func-wallet-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/04_sharded_tgbtc/jetton-wallet.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/04_sharded_tgbtc/JettonWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/04_sharded_tgbtc/func-wallet-comby \
  --timeout 300 > tmp/tolk-bench/04_sharded_tgbtc/func-wallet-comby/analyze.out 2>&1
```

### 05 Wallet V5

```bash
# --- wallet_v5.fc ---
mkdir -p tmp/tolk-bench/05_wallet-v5/func-wallet-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/05_wallet-v5/wallet_v5.fc func --only func.rules --mutantDir tmp/tolk-bench/05_wallet-v5/func-wallet-only > tmp/tolk-bench/05_wallet-v5/func-wallet-only/check.out 2>&1

mkdir -p tmp/tolk-bench/05_wallet-v5/func-wallet-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/05_wallet-v5/wallet_v5.fc func --mutantDir tmp/tolk-bench/05_wallet-v5/func-wallet-all > tmp/tolk-bench/05_wallet-v5/func-wallet-all/check.out 2>&1

mkdir -p tmp/tolk-bench/05_wallet-v5/func-wallet-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/05_wallet-v5/wallet_v5.fc func --mutantDir tmp/tolk-bench/05_wallet-v5/func-wallet-comby --comby > tmp/tolk-bench/05_wallet-v5/func-wallet-comby/check.out 2>&1
```

```sh
# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_FunC/05_wallet-v5/wallet_v5.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/05_wallet-v5/WalletW5.spec.ts" \
  --mutantDir tmp/tolk-bench/05_wallet-v5/func-wallet-all \
  --timeout 300 > tmp/tolk-bench/05_wallet-v5/func-wallet-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/05_wallet-v5/wallet_v5.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/05_wallet-v5/WalletW5.spec.ts" \
  --mutantDir tmp/tolk-bench/05_wallet-v5/func-wallet-comby \
  --timeout 300 > tmp/tolk-bench/05_wallet-v5/func-wallet-comby/analyze.out 2>&1
```

### 06 Vesting

```bash
# --- vesting_wallet.fc ---
mkdir -p tmp/tolk-bench/06_vesting/func-vesting-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/06_vesting/vesting_wallet.fc func --only func.rules --mutantDir tmp/tolk-bench/06_vesting/func-vesting-only > tmp/tolk-bench/06_vesting/func-vesting-only/check.out 2>&1

mkdir -p tmp/tolk-bench/06_vesting/func-vesting-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/06_vesting/vesting_wallet.fc func --mutantDir tmp/tolk-bench/06_vesting/func-vesting-all > tmp/tolk-bench/06_vesting/func-vesting-all/check.out 2>&1

mkdir -p tmp/tolk-bench/06_vesting/func-vesting-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/06_vesting/vesting_wallet.fc func --mutantDir tmp/tolk-bench/06_vesting/func-vesting-comby --comby > tmp/tolk-bench/06_vesting/func-vesting-comby/check.out 2>&1
```

```sh
# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_FunC/06_vesting/vesting_wallet.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/06_vesting/VestingWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/06_vesting/func-vesting-all \
  --timeout 300 > tmp/tolk-bench/06_vesting/func-vesting-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/06_vesting/vesting_wallet.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/06_vesting/VestingWallet.spec.ts" \
  --mutantDir tmp/tolk-bench/06_vesting/func-vesting-comby \
  --timeout 300 > tmp/tolk-bench/06_vesting/func-vesting-comby/analyze.out 2>&1
```

### 07 Telemint

```bash
# --- nft-collection-no-dns.fc ---
mkdir -p tmp/tolk-bench/07_telemint/func-collection-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/07_telemint/nft-collection-no-dns.fc func --only func.rules --mutantDir tmp/tolk-bench/07_telemint/func-collection-only > tmp/tolk-bench/07_telemint/func-collection-only/check.out 2>&1

mkdir -p tmp/tolk-bench/07_telemint/func-collection-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/07_telemint/nft-collection-no-dns.fc func --mutantDir tmp/tolk-bench/07_telemint/func-collection-all > tmp/tolk-bench/07_telemint/func-collection-all/check.out 2>&1

mkdir -p tmp/tolk-bench/07_telemint/func-collection-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/07_telemint/nft-collection-no-dns.fc func --mutantDir tmp/tolk-bench/07_telemint/func-collection-comby --comby > tmp/tolk-bench/07_telemint/func-collection-comby/check.out 2>&1

# --- nft-item-no-dns-cheap.fc ---
mkdir -p tmp/tolk-bench/07_telemint/func-item-only
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/07_telemint/nft-item-no-dns-cheap.fc func --only func.rules --mutantDir tmp/tolk-bench/07_telemint/func-item-only > tmp/tolk-bench/07_telemint/func-item-only/check.out 2>&1

mkdir -p tmp/tolk-bench/07_telemint/func-item-all
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/07_telemint/nft-item-no-dns-cheap.fc func --mutantDir tmp/tolk-bench/07_telemint/func-item-all > tmp/tolk-bench/07_telemint/func-item-all/check.out 2>&1

mkdir -p tmp/tolk-bench/07_telemint/func-item-comby
python -m universalmutator.genmutants examples/tolk-bench/contracts_FunC/07_telemint/nft-item-no-dns-cheap.fc func --mutantDir tmp/tolk-bench/07_telemint/func-item-comby --comby > tmp/tolk-bench/07_telemint/func-item-comby/check.out 2>&1
```

```sh
# --- analyze_mutants ---
analyze_mutants examples/tolk-bench/contracts_FunC/07_telemint/nft-collection-no-dns.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/07_telemint/Nft.spec.ts" \
  --mutantDir tmp/tolk-bench/07_telemint/func-collection-all \
  --timeout 300 > tmp/tolk-bench/07_telemint/func-collection-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/07_telemint/nft-collection-no-dns.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/07_telemint/Nft.spec.ts" \
  --mutantDir tmp/tolk-bench/07_telemint/func-collection-comby \
  --timeout 300 > tmp/tolk-bench/07_telemint/func-collection-comby/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/07_telemint/nft-item-no-dns-cheap.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/07_telemint/Nft.spec.ts" \
  --mutantDir tmp/tolk-bench/07_telemint/func-item-all \
  --timeout 300 > tmp/tolk-bench/07_telemint/func-item-all/analyze.out 2>&1

analyze_mutants examples/tolk-bench/contracts_FunC/07_telemint/nft-item-no-dns-cheap.fc \
  "cd examples/tolk-bench && npx jest --runInBand tests/07_telemint/Nft.spec.ts" \
  --mutantDir tmp/tolk-bench/07_telemint/func-item-comby \
  --timeout 300 > tmp/tolk-bench/07_telemint/func-item-comby/analyze.out 2>&1
```

## Tact

### Base

```sh
# Build + test target used by analyze_mutants
cd examples/jetton && yarn build:base && npx jest --runInBand src/tests/base -t 'Base Jetton'

# --- jetton-minter.tact ---
mkdir -p tmp/jetton/base-minter-all
UM_TACT_CMD='cd examples/jetton && npx tact --config ./tact.config.json --project Jetton' \
python -m universalmutator.genmutants examples/jetton/src/contracts/base/jetton-minter.tact tact \
  --mutantDir tmp/jetton/base-minter-all \
  > tmp/jetton/base-minter-all/check.out 2>&1

mkdir -p tmp/jetton/base-minter-comby
UM_TACT_CMD='cd examples/jetton && npx tact --config ./tact.config.json --project Jetton' \
python -m universalmutator.genmutants examples/jetton/src/contracts/base/jetton-minter.tact tact \
  --mutantDir tmp/jetton/base-minter-comby \
  --comby \
  > tmp/jetton/base-minter-comby/check.out 2>&1

# --- jetton-wallet.tact ---
mkdir -p tmp/jetton/base-wallet-all
UM_TACT_CMD='cd examples/jetton && npx tact --config ./tact.config.json --project Jetton' \
python -m universalmutator.genmutants examples/jetton/src/contracts/base/jetton-wallet.tact tact \
  --mutantDir tmp/jetton/base-wallet-all \
  > tmp/jetton/base-wallet-all/check.out 2>&1

mkdir -p tmp/jetton/base-wallet-comby
UM_TACT_CMD='cd examples/jetton && npx tact --config ./tact.config.json --project Jetton' \
python -m universalmutator.genmutants examples/jetton/src/contracts/base/jetton-wallet.tact tact \
  --mutantDir tmp/jetton/base-wallet-comby \
  --comby \
  > tmp/jetton/base-wallet-comby/check.out 2>&1
```

```sh
# --- analyze_mutants ---
analyze_mutants examples/jetton/src/contracts/base/jetton-minter.tact \
  "cd examples/jetton && yarn build:base && npx jest --runInBand src/tests/base -t 'Base Jetton'" \
  --mutantDir tmp/jetton/base-minter-all \
  --timeout 300 > tmp/jetton/base-minter-all/analyze.out 2>&1

analyze_mutants examples/jetton/src/contracts/base/jetton-minter.tact \
  "cd examples/jetton && yarn build:base && npx jest --runInBand src/tests/base -t 'Base Jetton'" \
  --mutantDir tmp/jetton/base-minter-comby \
  --timeout 300 > tmp/jetton/base-minter-comby/analyze.out 2>&1

analyze_mutants examples/jetton/src/contracts/base/jetton-wallet.tact \
  "cd examples/jetton && yarn build:base && npx jest --runInBand src/tests/base -t 'Base Jetton'" \
  --mutantDir tmp/jetton/base-wallet-all \
  --timeout 300 > tmp/jetton/base-wallet-all/analyze.out 2>&1

analyze_mutants examples/jetton/src/contracts/base/jetton-wallet.tact \
  "cd examples/jetton && yarn build:base && npx jest --runInBand src/tests/base -t 'Base Jetton'" \
  --mutantDir tmp/jetton/base-wallet-comby \
  --timeout 300 > tmp/jetton/base-wallet-comby/analyze.out 2>&1
```

### Governance

```sh
# Build + test target used by analyze_mutants
cd examples/jetton && yarn build:governance && npx jest --runInBand src/tests/governance-tests

# --- jetton-minter.tact ---
mkdir -p tmp/jetton/governance-minter-all
UM_TACT_CMD='cd examples/jetton && npx tact --config ./tact.config.json --project Governance' \
python -m universalmutator.genmutants examples/jetton/src/contracts/governance/jetton-minter.tact tact \
  --mutantDir tmp/jetton/governance-minter-all \
  > tmp/jetton/governance-minter-all/check.out 2>&1

mkdir -p tmp/jetton/governance-minter-comby
UM_TACT_CMD='cd examples/jetton && npx tact --config ./tact.config.json --project Governance' \
python -m universalmutator.genmutants examples/jetton/src/contracts/governance/jetton-minter.tact tact \
  --mutantDir tmp/jetton/governance-minter-comby \
  --comby \
  > tmp/jetton/governance-minter-comby/check.out 2>&1

# --- jetton-wallet.tact ---
mkdir -p tmp/jetton/governance-wallet-all
UM_TACT_CMD='cd examples/jetton && npx tact --config ./tact.config.json --project Governance' \
python -m universalmutator.genmutants examples/jetton/src/contracts/governance/jetton-wallet.tact tact \
  --mutantDir tmp/jetton/governance-wallet-all \
  > tmp/jetton/governance-wallet-all/check.out 2>&1

mkdir -p tmp/jetton/governance-wallet-comby
UM_TACT_CMD='cd examples/jetton && npx tact --config ./tact.config.json --project Governance' \
python -m universalmutator.genmutants examples/jetton/src/contracts/governance/jetton-wallet.tact tact \
  --mutantDir tmp/jetton/governance-wallet-comby \
  --comby \
  > tmp/jetton/governance-wallet-comby/check.out 2>&1

```

```sh
# --- analyze_mutants ---
analyze_mutants examples/jetton/src/contracts/governance/jetton-minter.tact \
  "cd examples/jetton && yarn build:governance && npx jest --runInBand src/tests/governance-tests" \
  --mutantDir tmp/jetton/governance-minter-all \
  --timeout 300 > tmp/jetton/governance-minter-all/analyze.out 2>&1

analyze_mutants examples/jetton/src/contracts/governance/jetton-minter.tact \
  "cd examples/jetton && yarn build:governance && npx jest --runInBand src/tests/governance-tests" \
  --mutantDir tmp/jetton/governance-minter-comby \
  --timeout 300 > tmp/jetton/governance-minter-comby/analyze.out 2>&1

analyze_mutants examples/jetton/src/contracts/governance/jetton-wallet.tact \
  "cd examples/jetton && yarn build:governance && npx jest --runInBand src/tests/governance-tests" \
  --mutantDir tmp/jetton/governance-wallet-all \
  --timeout 300 > tmp/jetton/governance-wallet-all/analyze.out 2>&1

analyze_mutants examples/jetton/src/contracts/governance/jetton-wallet.tact \
  "cd examples/jetton && yarn build:governance && npx jest --runInBand src/tests/governance-tests" \
  --mutantDir tmp/jetton/governance-wallet-comby \
  --timeout 300 > tmp/jetton/governance-wallet-comby/analyze.out 2>&1
```
