# Mutant Generation Report (tolk-bench + jetton tact)

## Summary Table by Contract

| Group             | Contract        | Static Gen | Static Valid | Static Invalid | Comby Gen | Comby Valid | Comby Invalid |
| ----------------- | --------------- | ---------: | -----------: | -------------: | --------: | ----------: | ------------: |
| 01_jetton         | func-minter     |         92 |            0 |             92 |        90 |           0 |            84 |
| 01_jetton         | func-wallet     |        156 |          143 |             13 |       137 |         124 |            10 |
| 01_jetton         | tolk-minter     |         68 |           58 |             10 |        53 |          44 |             7 |
| 01_jetton         | tolk-wallet     |         95 |           88 |              7 |        82 |          73 |             7 |
| 02_nft            | func-collection |        116 |          106 |             10 |       110 |          99 |             7 |
| 02_nft            | func-item       |         90 |           84 |              6 |        82 |          76 |             5 |
| 02_nft            | tolk-collection |         71 |           66 |              5 |        57 |          53 |             3 |
| 02_nft            | tolk-item       |         68 |           54 |             14 |        62 |          48 |            13 |
| 03_notcoin        | func-minter     |        113 |          108 |              5 |        85 |          82 |             1 |
| 03_notcoin        | func-wallet     |        105 |          101 |              4 |        98 |          87 |             8 |
| 03_notcoin        | tolk-minter     |        110 |           95 |             15 |        74 |          62 |            10 |
| 03_notcoin        | tolk-wallet     |         98 |           87 |             11 |        80 |          66 |            11 |
| 04_sharded_tgbtc  | func-wallet     |        104 |          101 |              3 |        90 |          80 |             7 |
| 04_sharded_tgbtc  | tolk-wallet     |         96 |           85 |             11 |        78 |          64 |            11 |
| 05_wallet-v5      | func-wallet     |        189 |          163 |             26 |       184 |         146 |            38 |
| 05_wallet-v5      | tolk-wallet     |        128 |          112 |             16 |       119 |         102 |            17 |
| 06_vesting        | func-vesting    |        278 |          242 |             36 |       222 |         173 |            47 |
| 06_vesting        | tolk-vesting    |         81 |           75 |              6 |        58 |          54 |             2 |
| 07_telemint       | func-collection |         71 |           65 |              6 |        63 |          56 |             7 |
| 07_telemint       | func-item       |        204 |          193 |             11 |       175 |         157 |            17 |
| 07_telemint       | tolk-collection |         67 |           51 |             16 |        62 |          40 |            20 |
| 07_telemint       | tolk-item       |        306 |          232 |             74 |       256 |         180 |            70 |
| jetton/base       | tact-minter     |        124 |           88 |             36 |        90 |          80 |            10 |
| jetton/base       | tact-wallet     |        151 |          111 |             40 |       111 |         100 |            11 |
| jetton/governance | tact-minter     |        176 |          134 |             42 |       125 |         107 |            18 |
| jetton/governance | tact-wallet     |        155 |          110 |             45 |       109 |          95 |            14 |
| **TOTAL**         |                 |   **3149** |     **2589** |        **560** |  **2752** |    **2248** |       **455** |

## Breakdown by Language

| Language | Static Gen | Static Valid | Static Invalid | Comby Gen | Comby Valid | Comby Invalid |
| -------- | ---------: | -----------: | -------------: | --------: | ----------: | ------------: |
| func     |       1518 |         1306 |            212 |      1336 |        1080 |           231 |
| tact     |        606 |          443 |            163 |       435 |         382 |            53 |
| tolk     |       1188 |         1003 |            185 |       981 |         786 |           171 |

## Key observations

1. **FunC minter (01_jetton) has 0 valid mutants.**  
   All generated mutants, both static and Comby, fail to compile.  
   Most likely, this minter needs a special wrapper or compile configuration.

2. **Comby generates fewer mutants than static+universal.**  
   On average, Comby produces about 12.6% fewer mutants (`2752` vs `3149`).  
   This is expected: Comby templates are more conservative than regex rules.

3. **After adding Tact, static still produces more mutants, but Comby remains competitive on compile-valid output.**
   - Static: 82.2% valid (`2589 / 3149`)
   - Comby: 81.7% valid (`2248 / 2752`)

4. **Tact shows the largest static/comby compile-valid gap.**
   - Static valid rate: 73.1% (`443 / 606`)
   - Comby valid rate: 87.8% (`382 / 435`)

5. **Largest contract by mutant count:**
   - Static: `07_telemint/tolk-item` — `306` mutants
   - Comby: `07_telemint/tolk-item` — `256` mutants
