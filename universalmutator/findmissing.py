from __future__ import print_function
import argparse
import glob

from universalmutator import utils


def main():

    parser = argparse.ArgumentParser(prog="find_missing",
                                     description="Show mutants present in one directory but not another.")
    parser.add_argument("f", help="base source filename (e.g. foo.py)")
    parser.add_argument("d1", help="first mutant directory")
    parser.add_argument("d2", help="second mutant directory")
    parsed = parser.parse_args()

    f = parsed.f
    d1 = parsed.d1
    d2 = parsed.d2

    fsplit = f.split(".")
    pattern = "/" + fsplit[0] + ".mutant.*." + fsplit[-1]
    d1files = glob.glob(d1 + pattern)
    d2files = glob.glob(d2 + pattern)
    d1contents = []
    d2contents = []
    d1all = []
    d2all = []
    for d1f in d1files:
        with open(d1f, "r") as d1c:
            r = d1c.read()
            if r not in d1all:
                d1all.append(r)
            else:
                print(d1f, "IS REDUNDANT!")
            d1contents.append((d1f, r))
    for d2f in d2files:
        with open(d2f, "r") as d2c:
            r = d2c.read()
            if r not in d2all:
                d2all.append(r)
            else:
                print(d2f, "IS REDUNDANT!")
            d2contents.append((d2f, r))

    just1c = list(map(lambda x: x[1], d1contents))
    just2c = list(map(lambda x: x[1], d2contents))
    print("="*80)
    for (mf, c) in d1contents:
        if c not in just2c:
            m = utils.readMutant(mf, f)
            utils.show(m)
    print("="*80)
    for (mf, c) in d2contents:
        if c not in just1c:
            m = utils.readMutant(mf, f)
            utils.show(m)


if __name__ == '__main__':
    main()
