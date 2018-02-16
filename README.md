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

A MORE COMPLEX EXAMPLE
======================

Sometimes the mutated code needs to be built with a more complicated command than a simple compiler call, and of course you want help discovering which mutants are killed and not killed.  For example, to mutate and test mutants for the mandelbrot plotting example included in Programming Rust, just do this:


    git clone https://github.com/ProgrammingRust/mandelbrot
    cd mandelbrot
    cargo build
    target/debug/mandelbrot origmandel.png 1000x750 -1.20,0.35 -1,0.20
    mkdir mutants
    mutate src/main.rs --mutantDir mutants
    analyze_mutants src/main.rs "cargo clean; cargo build; rm mandel.png; target/debug/mandelbrot mandel.png 1000x750 -1.20,0.35 -1,0.20; diff mandel.png origmandel.png" --mutantDir mutants


MORE INFORMATON
===============

For much more information, again see https://www.cefns.nau.edu/~adg326/icse18t.pdf -- demo/tool paper at ICSE 18.

The aim of this project is partly to see how quickly mutation can be applied to new languages, partly how much the work of a tool can be
offloaded to the compiler / test analysis tools.

Authors:  Alex Groce, Josie Holmes, Darko Marinov, August Shi, Lingming Zhang
