# Mutation Analysis Report (Tolk)

## Summary Table

| Contract                             | Mode |   Killed | NotKilled |    Total | Mutation Score |
| ------------------------------------ | ---- | -------: | --------: | -------: | -------------: |
| 01_jetton / tolk-minter-all          | -    |       35 |        23 |       58 |         60.34% |
| 01_jetton / tolk-minter-comby        | -    |       23 |        21 |       44 |         52.27% |
| 01_jetton / tolk-wallet-all          | -    |       64 |        24 |       88 |         72.73% |
| 01_jetton / tolk-wallet-comby        | -    |       50 |        23 |       73 |         68.49% |
| 02_nft / tolk-collection-all         | -    |       41 |        25 |       66 |         62.12% |
| 02_nft / tolk-collection-comby       | -    |       42 |        11 |       53 |         79.25% |
| 02_nft / tolk-item-all               | -    |       34 |        20 |       54 |         62.96% |
| 02_nft / tolk-item-comby             | -    |       40 |         8 |       48 |         83.33% |
| 03_notcoin / tolk-minter-all         | -    |       83 |        12 |       95 |         87.37% |
| 03_notcoin / tolk-minter-comby       | -    |       29 |        33 |       62 |         46.77% |
| 03_notcoin / tolk-wallet-all         | -    |       81 |         6 |       87 |         93.10% |
| 03_notcoin / tolk-wallet-comby       | -    |       52 |        14 |       66 |         78.79% |
| 04_sharded_tgbtc / tolk-wallet-all   | -    |       69 |        16 |       85 |         81.18% |
| 04_sharded_tgbtc / tolk-wallet-comby | -    |       52 |        12 |       64 |         81.25% |
| 05_wallet-v5 / tolk-wallet-all       | -    |       93 |        19 |      112 |         83.04% |
| 05_wallet-v5 / tolk-wallet-comby     | -    |       84 |        18 |      102 |         82.35% |
| 06_vesting / tolk-vesting-all        | -    |       53 |        22 |       75 |         70.67% |
| 06_vesting / tolk-vesting-comby      | -    |       33 |        21 |       54 |         61.11% |
| 07_telemint / tolk-collection-all    | -    |       43 |         8 |       51 |         84.31% |
| 07_telemint / tolk-collection-comby  | -    |       31 |         9 |       40 |         77.50% |
| 07_telemint / tolk-item-all          | -    |      160 |        72 |      232 |         68.97% |
| 07_telemint / tolk-item-comby        | -    |      128 |        52 |      180 |         71.11% |
| **TOTAL**                            |      | **1320** |   **469** | **1789** |     **73.78%** |

## Comparison of Static vs. Comby by group

| Группа                         | Контракт | Static Score | Comby Score |       Δ |
| ------------------------------ | -------- | -----------: | ----------: | ------: |
| 01_jetton / tolk-minter        |          |       60.34% |      52.27% |  -8.07% |
| 01_jetton / tolk-wallet        |          |       72.73% |      68.49% |  -4.23% |
| 02_nft / tolk-collection       |          |       62.12% |      79.25% | +17.12% |
| 02_nft / tolk-item             |          |       62.96% |      83.33% | +20.37% |
| 03_notcoin / tolk-minter       |          |       87.37% |      46.77% | -40.59% |
| 03_notcoin / tolk-wallet       |          |       93.10% |      78.79% | -14.32% |
| 04_sharded_tgbtc / tolk-wallet |          |       81.18% |      81.25% |  +0.07% |
| 05_wallet-v5 / tolk-wallet     |          |       83.04% |      82.35% |  -0.68% |
| 06_vesting / tolk-vesting      |          |       70.67% |      61.11% |  -9.56% |
| 07_telemint / tolk-collection  |          |       84.31% |      77.50% |  -6.81% |
| 07_telemint / tolk-item        |          |       68.97% |      71.11% |  +2.15% |

## Observations

1. **Best mutation score:** 03_notcoin/tolk-wallet-all/analyze.out — 93.10% (81/87)
2. **Worst mutation score:** 03_notcoin/tolk-minter-comby/analyze.out — 46.77% (29/62)
3. **Overall mutation score across all Tolk contracts:** 73.78% (1320/1789)
4. **Average score (static):** 75.16%
   **Average score (comby):** 71.11%
   **Difference:** -4.05%
