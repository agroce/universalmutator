This is a tool based purely on regexp-specified rewrite of code lines for mutation generation, including
multi-language rules aided by special rules for languages or even projects.

More information on this project can be found at: https://www.cefns.nau.edu/~adg326/icse18t.pdf 

HOW TO USE IT
=============

To use this, you should really just do:

`pip install universalmutator`

then

`mutate --help`

SIMPLE EXAMPLE USAGE
====================

`mutate foo.py`

or

`mutate foo.swift`

should, if you have the appropriate compilers installed, generate a bunch of valid, non-trivially redundant, mutants.

It will, right now, also have the side effect of executing foo.py if it is a script, not a module,
many times, and leave some junk files in the directory, just FYI.

MORE INFORMATON
===============

For much more information, again see https://www.cefns.nau.edu/~adg326/icse18t.pdf -- demo/tool paper at ICSE 18.

The aim of this project is partly to see how quickly mutation can be applied to new languages, partly how much the work of a tool can be
offloaded to the compiler / test analysis tools.

Authors:  Alex Groce, Josie Holmes, Darko Marinov, August Shi, Lingming Zhang
