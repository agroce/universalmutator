Start on a tool based purely on regexp-specified rewrite of code lines for mutation generation, including
multi-language rules aided by special rules for languages or even projects.

HOW TO USE IT

To use this, you should really just do:

`pip install universalmutator`

then

`mutate --help`

SIMPLE EXAMPLE

`mutate foo.py`

or

`mutate foo.swift`

should, if you have the appropriate compilers installed, generate a bunch of valid, non-trivially redundant, mutants.

MORE INFORMATON

Aim is partly to see how quickly mutation can be applied to new languages, partly how much work of a tool can be
offloaded to the compiler / test analysis tools.

Authors:  Alex Groce, Darko Marinov, Lingming Zhang
