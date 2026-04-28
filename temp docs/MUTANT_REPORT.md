# Отчет по генерации мутантов (tolk-bench)

## Сводная таблица по контрактам

| Группа           | Контракт        | Static Gen | Static Valid | Static Invalid | Comby Gen | Comby Valid | Comby Invalid |
| ---------------- | --------------- | ---------: | -----------: | -------------: | --------: | ----------: | ------------: |
| 01_jetton        | func-minter     |         92 |            0 |             92 |        90 |           0 |            84 |
| 01_jetton        | func-wallet     |        156 |          143 |             13 |       137 |         124 |            10 |
| 01_jetton        | tolk-minter     |         68 |           58 |             10 |        53 |          44 |             7 |
| 01_jetton        | tolk-wallet     |         95 |           88 |              7 |        82 |          73 |             7 |
| 02_nft           | func-collection |        116 |          106 |             10 |       110 |          99 |             7 |
| 02_nft           | func-item       |         90 |           84 |              6 |        82 |          76 |             5 |
| 02_nft           | tolk-collection |         71 |           66 |              5 |        57 |          53 |             3 |
| 02_nft           | tolk-item       |         68 |           54 |             14 |        62 |          48 |            13 |
| 03_notcoin       | func-minter     |        113 |          108 |              5 |        85 |          82 |             1 |
| 03_notcoin       | func-wallet     |        105 |          101 |              4 |        98 |          87 |             8 |
| 03_notcoin       | tolk-minter     |        110 |           95 |             15 |        74 |          62 |            10 |
| 03_notcoin       | tolk-wallet     |         98 |           87 |             11 |        80 |          66 |            11 |
| 04_sharded_tgbtc | func-wallet     |        104 |          101 |              3 |        90 |          80 |             7 |
| 04_sharded_tgbtc | tolk-wallet     |         96 |           85 |             11 |        78 |          64 |            11 |
| 05_wallet-v5     | func-wallet     |        189 |          163 |             26 |       184 |         146 |            38 |
| 05_wallet-v5     | tolk-wallet     |        128 |          112 |             16 |       119 |         102 |            17 |
| 06_vesting       | func-vesting    |        278 |          242 |             36 |       222 |         173 |            47 |
| 06_vesting       | tolk-vesting    |         81 |           75 |              6 |        58 |          54 |             2 |
| 07_telemint      | func-collection |         71 |           65 |              6 |        63 |          56 |             7 |
| 07_telemint      | func-item       |        204 |          193 |             11 |       175 |         157 |            17 |
| 07_telemint      | tolk-collection |         67 |           51 |             16 |        62 |          40 |            20 |
| 07_telemint      | tolk-item       |        306 |          232 |             74 |       256 |         180 |            70 |
| **ИТОГО**        |                 |   **2706** |     **2309** |        **397** |  **2317** |    **1866** |       **402** |

## Разбивка по языкам

| Язык | Static Gen | Static Valid | Static Invalid | Comby Gen | Comby Valid | Comby Invalid |
| ---- | ---------: | -----------: | -------------: | --------: | ----------: | ------------: |
| func |       1518 |         1306 |            212 |      1336 |        1080 |           231 |
| tolk |       1188 |         1003 |            185 |       981 |         786 |           171 |

## Ключевые наблюдения

1. **FunC minter (01_jetton) — 0 valid мутантов.**
   Все сгенерированные мутанты (static и comby) не компилируются.
   Вероятно, minter требует особой конфигурации wrapper/compile.

2. **Comby генерирует меньше мутантов, чем static+universal.**
   В среднем comby дает ~14.4% меньше мутантов (2317 vs 2706).
   Это ожидаемо: шаблонные правила comby более консервативны, чем regex.

3. **Процент компилируемых мутантов примерно сопоставим:**
   - Static: 85.3% (2309/2706)
   - Comby: 80.5% (1866/2317)

4. **Наибольший контракт по мутантам:**
   - Static: 07_telemint/tolk-item — 306 мутантов
   - Comby: 07_telemint/tolk-item — 256 мутантов
