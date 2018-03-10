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

Sometimes the mutated code needs to be built with a more complicated command than a simple compiler call, and of course you want help discovering which mutants are killed and not killed.  For example, to mutate and test mutants for the mandelbrot plotting example included in _Programming Rust_ (http://shop.oreilly.com/product/0636920040385.do), just do this:


    git clone https://github.com/ProgrammingRust/mandelbrot
    cd mandelbrot
    cargo build
    target/debug/mandelbrot origmandel.png 1000x750 -1.20,0.35 -1,0.20
    mkdir mutants
    mutate src/main.rs --mutantDir mutants --noCheck
    analyze_mutants src/main.rs "cargo clean; cargo build; rm mandel.png; target/debug/mandelbrot mandel.png 1000x750 -1.20,0.35 -1,0.20; diff mandel.png origmandel.png" --mutantDir mutants

(It will go faster if you edit `main.rs` to lower the maximum number of threads used to something like 8, not 90.) At the moment, this won't use any Trivial Compiler Equivalence, but still kills about 60% of the 1000+ mutants. The killed mutant filenames will be in `killed.txt` and the non-killed ones in `not-killed.txt`.

Working with something like maven is very similar, except you can probably edit the complicated build/clean stuff to just a 'mvn test' or similar.

CURRENTLY SUPPORTED LANGUAGES
=============================

The tool will likely mutate other things, if you tell it they are "c" or something, but there is auto-detection based on file ending and specific rule support for:

C
C++
Java
Python
Swift
Rust
Solidity

All but C and C++ will try, by default, to compile the mutated file and use TCE to detect redundancy.  Of course, build dependencies may frustrate this process, in which case --noCheck will turn off TCE and just dump all the mutants in the directory, for pruning using a real build process.  In the long run, we plan to integrate with standard build systems to avoid this problem.

MORE INFORMATON
===============

For much more information, again see https://www.cefns.nau.edu/~adg326/icse18t.pdf -- demo/tool paper at ICSE 18.

The aim of this project is partly to see how quickly mutation can be applied to new languages, partly how much the work of a tool can be
offloaded to the compiler / test analysis tools.

Authors:  Alex Groce, Josie Holmes, Darko Marinov, August Shi, Lingming Zhang
