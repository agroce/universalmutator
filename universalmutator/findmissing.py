from __future__ import print_function
import glob
import sys

import universalmutator.utils as utils


def main():

    f = sys.argv[1]
    d1 = sys.argv[2]
    d2 = sys.argv[3]

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
