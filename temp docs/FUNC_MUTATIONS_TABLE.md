# FunC Mutation Table

Current for `universalmutator/static/func.rules` and `universalmutator/comby/func.rules`.
The default FunC flow uses `ton_common.rules` + `func.rules`; shared boolean/comparison/assignment/while/break rules are documented separately in `TON_COMMON_MUTATIONS_TABLE.md`.

## Summary

| File                | Rule Count | Notes                                                        |
| ------------------- | ---------: | ------------------------------------------------------------ |
| `static/func.rules` |        145 | FunC-specific regex layer                                    |
| `comby/func.rules`  |        156 | Comby equivalent for syntax-aware surface mutations and guarded call-site swaps |
| `ton_common.rules`  |         36 | shared layer loaded before `func.rules`                      |

## Short Table

| Status  | Layer          | Construct                         | Rule                                                                                   | Effect                                                                                                           | Risk          |
| ------- | -------------- | --------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------- |
| Present | regex + Comby  | `#include`, `;;`                  | `#include -> DO_NOT_MUTATE`, `;; -> SKIP_MUTATING_REST`                                | avoids mutating imports and comment tails                                                                        | low           |
| Present | regex-only     | comment replacement               | statement-only `line -> ;; line`                                                       | comments out simple standalone statements; does not touch `{}`, declarations, `return`, `var`, or control-flow headers | medium        |
| Present | regex + Comby  | FunC `if` forcing                 | `if (cond) -> if (0) / if (1)`                                                         | forces branches via FunC integer booleans                                                                        | high          |
| Present | regex + Comby  | throw helpers                     | `throw_if <-> throw_unless`, `throw_arg_if <-> throw_arg_unless`, uppercase marker swaps | inverts guard-style abort helpers                                                                              | high          |
| Present | regex + Comby  | bitwise operator shuffle          | guarded `^ -> & / \|`, `& -> ^`, `\| -> ^`                                             | changes bitwise expressions without breaking `^/`, `^%`, `^/=`                                                 | medium        |
| Present | regex + Comby  | FunC division assignment          | `/= <-> ~/= / ^/=` with guards for plain `/=`                                          | changes rounding mode assignments                                                                                | high          |
| Present | regex + Comby  | FunC division operator            | `/ <-> ~/ / ^/` with guards for plain `/`                                              | changes rounding mode expressions                                                                                | high          |
| Present | regex + Comby  | FunC modulo assignment/operator   | `%= <-> ~%= / ^%=`, `% <-> ~% / ^%`                                                    | changes modulo rounding mode                                                                                     | high          |
| Present | regex + Comby  | `ifnot`, `until`, `repeat`        | `ifnot -> 0 / 1`, `until -> 0`, `repeat -> 0`                                          | changes branch and loop reachability                                                                             | high          |
| Present | regex + Comby  | function specifiers               | `inline <-> inline_ref`, remove `inline/inline_ref/impure`                             | changes inlining and side-effect markers                                                                         | high          |
| Removed | regex + Comby  | `method_id` zeroing               | `method_id(...) -> method_id(0)` removed                                               | the rule produced persistent compile-invalid mutants in FunC fixtures                                            | high          |
| Present | regex + Comby  | gas/state helpers                 | `accept_message();`, `commit();`, `set_code(...); -> ;`                                | removes important state/gas operations                                                                           | high          |
| Present | regex + Comby  | time/random helpers               | `now -> cur_lt`, `cur_lt <-> block_lt`, `random <-> get_seed`                          | changes the source of time and randomness                                                                        | high          |
| Present | regex + Comby  | load/preload helpers              | `load_* <-> preload_*`, but `load_* -> preload_*` not after `~`                        | switches between mutating and non-mutating reads                                                                 | high          |
| Present | regex + Comby  | signedness of load/store          | `load_uint <-> load_int`, `store_uint <-> store_int`                                   | changes signed/unsigned serialization semantics                                                                  | high          |
| Present | regex + Comby  | store zeroing                     | `.store_*` and function-style `store_*` payload -> `0`                                 | zeros stored coins/int/uint payloads                                                                             | high          |
| Present | regex + Comby  | modifying vs non-modifying notation | `.load_* <-> ~load_*`, `.store_* <-> ~store_*`                                       | changes whether the receiver is updated                                                                          | high          |
| Present | regex + Comby  | slice/builder inspection          | `slice_refs <-> slice_bits`, `builder_refs <-> builder_bits`, `slice_empty?` family    | changes slice/builder state checks                                                                               | high          |
| Present | regex + Comby  | dict signedness                   | `idict_* <-> udict_*`                                                                   | changes dictionary API signedness                                                                                | very high     |
| Present | regex + Comby  | numeric builtins                  | `divmod <-> moddiv`, `muldiv -> muldivr -> muldivc`, `muldivmod -> divmod`, `*_at` family | changes rounding, result shape, and tuple access                                                             | very high     |
| Present | regex + Comby  | send/reserve modes                | numeric mode literals in `send_raw_message`, `raw_reserve`, `raw_reserve_extra`        | changes message sending and reserve flags                                                                        | very high     |
