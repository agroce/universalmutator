# Mutation Analysis Report (Tolk, FunC, Tact)

Completed `analyze_mutants` runs found under `tmp/tolk-bench` and `tmp/jetton`.

## Totals by Language

| Language | Killed | NotKilled | Total | Mutation Score |
| -------- | -----: | --------: | ----: | -------------: |
| tolk     |   1320 |       469 |  1789 |         73.78% |
| func     |   1755 |       631 |  2386 |         73.55% |
| tact     |    610 |       215 |   825 |         73.94% |
| **TOTAL** | **3685** | **1315** | **5000** |     **73.70%** |

## Tolk

### Summary Table

| Group            | Contract        | Mode  | Killed | NotKilled | Total | Mutation Score |
| ---------------- | --------------- | ----- | -----: | --------: | ----: | -------------: |
| 01_jetton        | tolk-minter     | all   |     35 |        23 |    58 |         60.34% |
| 01_jetton        | tolk-minter     | comby |     23 |        21 |    44 |         52.27% |
| 01_jetton        | tolk-wallet     | all   |     64 |        24 |    88 |         72.73% |
| 01_jetton        | tolk-wallet     | comby |     50 |        23 |    73 |         68.49% |
| 02_nft           | tolk-collection | all   |     41 |        25 |    66 |         62.12% |
| 02_nft           | tolk-collection | comby |     42 |        11 |    53 |         79.25% |
| 02_nft           | tolk-item       | all   |     34 |        20 |    54 |         62.96% |
| 02_nft           | tolk-item       | comby |     40 |         8 |    48 |         83.33% |
| 03_notcoin       | tolk-minter     | all   |     83 |        12 |    95 |         87.37% |
| 03_notcoin       | tolk-minter     | comby |     29 |        33 |    62 |         46.77% |
| 03_notcoin       | tolk-wallet     | all   |     81 |         6 |    87 |         93.10% |
| 03_notcoin       | tolk-wallet     | comby |     52 |        14 |    66 |         78.79% |
| 04_sharded_tgbtc | tolk-wallet     | all   |     69 |        16 |    85 |         81.18% |
| 04_sharded_tgbtc | tolk-wallet     | comby |     52 |        12 |    64 |         81.25% |
| 05_wallet-v5     | tolk-wallet     | all   |     93 |        19 |   112 |         83.04% |
| 05_wallet-v5     | tolk-wallet     | comby |     84 |        18 |   102 |         82.35% |
| 06_vesting       | tolk-vesting    | all   |     53 |        22 |    75 |         70.67% |
| 06_vesting       | tolk-vesting    | comby |     33 |        21 |    54 |         61.11% |
| 07_telemint      | tolk-collection | all   |     43 |         8 |    51 |         84.31% |
| 07_telemint      | tolk-collection | comby |     31 |         9 |    40 |         77.50% |
| 07_telemint      | tolk-item       | all   |    160 |        72 |   232 |         68.97% |
| 07_telemint      | tolk-item       | comby |    128 |        52 |   180 |         71.11% |
| **TOTAL**        |                 |       | **1320** | **469** | **1789** |     **73.78%** |

### Comparison of Static vs. Comby by group

| Group            | Contract        | Static Score | Comby Score | Δ |
| ---------------- | --------------- | -----------: | ----------: | -: |
| 01_jetton        | tolk-minter     |       60.34% |      52.27% |  -8.07% |
| 01_jetton        | tolk-wallet     |       72.73% |      68.49% |  -4.23% |
| 02_nft           | tolk-collection |       62.12% |      79.25% | +17.12% |
| 02_nft           | tolk-item       |       62.96% |      83.33% | +20.37% |
| 03_notcoin       | tolk-minter     |       87.37% |      46.77% | -40.59% |
| 03_notcoin       | tolk-wallet     |       93.10% |      78.79% | -14.32% |
| 04_sharded_tgbtc | tolk-wallet     |       81.18% |      81.25% |  +0.07% |
| 05_wallet-v5     | tolk-wallet     |       83.04% |      82.35% |  -0.68% |
| 06_vesting       | tolk-vesting    |       70.67% |      61.11% |  -9.56% |
| 07_telemint      | tolk-collection |       84.31% |      77.50% |  -6.81% |
| 07_telemint      | tolk-item       |       68.97% |      71.11% |  +2.15% |

### Observations

1. **Best mutation score:** `03_notcoin / tolk-wallet / all` — 93.10% (81/87)
2. **Worst mutation score:** `03_notcoin / tolk-minter / comby` — 46.77% (29/62)
3. **Overall mutation score across all Tolk contracts:** 73.78% (1320/1789)
4. **Average score (static):** 75.16%
   **Average score (comby):** 71.11%
   **Difference:** -4.05%

## FunC

### Summary Table

| Group            | Contract        | Mode  | Killed | NotKilled | Total | Mutation Score |
| ---------------- | --------------- | ----- | -----: | --------: | ----: | -------------: |
| 01_jetton        | func-wallet     | all   |     92 |        51 |   143 |         64.34% |
| 01_jetton        | func-wallet     | comby |     76 |        48 |   124 |         61.29% |
| 02_nft           | func-collection | all   |     79 |        27 |   106 |         74.53% |
| 02_nft           | func-collection | comby |     72 |        27 |    99 |         72.73% |
| 02_nft           | func-item       | all   |     68 |        16 |    84 |         80.95% |
| 02_nft           | func-item       | comby |     56 |        20 |    76 |         73.68% |
| 03_notcoin       | func-minter     | all   |     81 |        27 |   108 |         75.00% |
| 03_notcoin       | func-minter     | comby |     71 |        11 |    82 |         86.59% |
| 03_notcoin       | func-wallet     | all   |     72 |        29 |   101 |         71.29% |
| 03_notcoin       | func-wallet     | comby |     56 |        31 |    87 |         64.37% |
| 04_sharded_tgbtc | func-wallet     | all   |     86 |        15 |   101 |         85.15% |
| 04_sharded_tgbtc | func-wallet     | comby |     69 |        11 |    80 |         86.25% |
| 05_wallet-v5     | func-wallet     | all   |    129 |        34 |   163 |         79.14% |
| 05_wallet-v5     | func-wallet     | comby |    114 |        32 |   146 |         78.08% |
| 06_vesting       | func-vesting    | all   |    150 |        92 |   242 |         61.98% |
| 06_vesting       | func-vesting    | comby |    102 |        71 |   173 |         58.96% |
| 07_telemint      | func-collection | all   |     54 |        11 |    65 |         83.08% |
| 07_telemint      | func-collection | comby |     49 |         7 |    56 |         87.50% |
| 07_telemint      | func-item       | all   |    159 |        34 |   193 |         82.38% |
| 07_telemint      | func-item       | comby |    120 |        37 |   157 |         76.43% |
| **TOTAL**        |                 |       | **1755** | **631** | **2386** |     **73.55%** |

### Comparison of Static vs. Comby by group

| Group            | Contract        | Static Score | Comby Score | Δ |
| ---------------- | --------------- | -----------: | ----------: | -: |
| 01_jetton        | func-wallet     |       64.34% |      61.29% |  -3.05% |
| 02_nft           | func-collection |       74.53% |      72.73% |  -1.80% |
| 02_nft           | func-item       |       80.95% |      73.68% |  -7.27% |
| 03_notcoin       | func-minter     |       75.00% |      86.59% | +11.59% |
| 03_notcoin       | func-wallet     |       71.29% |      64.37% |  -6.92% |
| 04_sharded_tgbtc | func-wallet     |       85.15% |      86.25% |  +1.10% |
| 05_wallet-v5     | func-wallet     |       79.14% |      78.08% |  -1.06% |
| 06_vesting       | func-vesting    |       61.98% |      58.96% |  -3.02% |
| 07_telemint      | func-collection |       83.08% |      87.50% |  +4.42% |
| 07_telemint      | func-item       |       82.38% |      76.43% |  -5.95% |

### Observations

1. **Best mutation score:** `07_telemint / func-collection / comby` — 87.50% (49/56)
2. **Worst mutation score:** `06_vesting / func-vesting / comby` — 58.96% (102/173)
3. **Overall mutation score across analyzed FunC contracts:** 73.55% (1755/2386)
4. **Average score (static):** 74.84%
   **Average score (comby):** 74.59%
   **Difference:** -0.26%
5. **No `01_jetton / func-minter` analyze run is present in `tmp/tolk-bench`.**

## Tact

### Summary Table

| Group              | Contract    | Mode  | Killed | NotKilled | Total | Mutation Score |
| ------------------ | ----------- | ----- | -----: | --------: | ----: | -------------: |
| jetton/base        | tact-minter | all   |     66 |        22 |    88 |         75.00% |
| jetton/base        | tact-minter | comby |     61 |        19 |    80 |         76.25% |
| jetton/base        | tact-wallet | all   |     78 |        33 |   111 |         70.27% |
| jetton/base        | tact-wallet | comby |     71 |        29 |   100 |         71.00% |
| jetton/governance  | tact-minter | all   |    109 |        25 |   134 |         81.34% |
| jetton/governance  | tact-minter | comby |     65 |        42 |   107 |         60.75% |
| jetton/governance  | tact-wallet | all   |     83 |        27 |   110 |         75.45% |
| jetton/governance  | tact-wallet | comby |     77 |        18 |    95 |         81.05% |
| **TOTAL**          |             |       | **610** | **215** | **825** |     **73.94%** |

### Comparison of Static vs. Comby by group

| Group             | Contract    | Static Score | Comby Score | Δ |
| ----------------- | ----------- | -----------: | ----------: | -: |
| jetton/base       | tact-minter |       75.00% |      76.25% |  +1.25% |
| jetton/base       | tact-wallet |       70.27% |      71.00% |  +0.73% |
| jetton/governance | tact-minter |       81.34% |      60.75% | -20.60% |
| jetton/governance | tact-wallet |       75.45% |      81.05% |  +5.60% |

### Observations

1. **Best mutation score:** `jetton/governance / tact-minter / all` — 81.34% (109/134)
2. **Worst mutation score:** `jetton/governance / tact-minter / comby` — 60.75% (65/107)
3. **Overall mutation score across all Tact contracts:** 73.94% (610/825)
4. **Average score (static):** 75.69%
   **Average score (comby):** 72.26%
   **Difference:** -3.42%
5. **Largest static/comby regression:** `jetton/governance / tact-minter` drops by 20.60 percentage points in `comby` mode.
