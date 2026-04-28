# Shared TON Mutation Table

Current for `universalmutator/static/ton_common.rules` and `universalmutator/comby/ton_common.rules`.
This ruleset is loaded first for Tact, FunC, and Tolk and contains only the families currently considered syntax-safe across all three languages.

## Summary

| File                      | Rule Count | Notes                                     |
| ------------------------- | ---------: | ----------------------------------------- |
| `static/ton_common.rules` |         36 | regex implementation using Python `re`    |
| `comby/ton_common.rules`  |         36 | Comby equivalent without language-specific rules |

## Short Table

| Status | Layer          | Construct                       | Rule                                         | Effect                                  | Risk   |
| ------ | -------------- | ------------------------------ | -------------------------------------------- | --------------------------------------- | ------ |
| Present | regex + Comby | boolean literals                | `true <-> false`                             | flips boolean constants                 | low    |
| Present | regex + Comby | comparisons                     | `== <-> !=`, `<= -> < / ==`, `>= -> > / ==` | changes guards and comparison boundaries | medium |
| Present | regex + Comby | logical operators               | `&& <-> \|\|`                                | changes conjunction/disjunction         | medium |
| Present | regex + Comby | `while` forcing                 | `while (cond) -> while (false)`              | makes a loop unreachable                | high   |
| Present | regex + Comby | loop control                    | `break <-> continue`                         | changes control flow inside loops       | high   |
| Present | regex + Comby | arithmetic assignment shuffle   | `+=`, `-=`, `*=`, `/=` are cross-swapped     | changes compound arithmetic updates     | medium |
| Present | regex + Comby | guarded `/=` shuffle            | `/= -> += / -= / *=`, but not after `~` or `^` | preserves FunC-specific `~/=` and `^/=` | medium |
| Present | regex + Comby | bitwise assignment shuffle      | `&=`, `\|=`, `^=` are cross-swapped          | changes compound bitwise updates        | medium |
| Present | regex + Comby | shift assignment/operator shuffle | `<<= <-> >>=`, `<< <-> >>`                 | changes shift direction                 | medium |

## What was moved out of common

`if` forcing is no longer shared: in Tolk we must avoid `is / !is` narrowing cases, and in FunC `!cond` is not a good universal form. Those `if` rules now live separately in `func.rules`, `tolk.rules`, and `tact.rules`.

Regex and Comby are synchronized at the family level. The main implementation difference is that Comby uses structured holes, so the guard for `/=` is expressed as the constrained hole `:[lhs~.*[^~^]\s*]/=:[rhs]`.
