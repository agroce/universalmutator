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
    for d1f in d1files:
        with open(d1f, "r") as d1c:
            d1contents.append((d1f, d1c.read()))
    for d2f in d2files:
        with open(d2f, "r") as d2c:
            d2contents.append((d2f, d2c.read()))

    just1c = list(map(lambda x: x[1], d1contents))
    just2c = list(map(lambda x: x[1], d2contents))
    print("="*80)
    for (mf, c) in d1contents:
        if c not in just2c:
            print(c)
            m = utils.readMutant(mf, f)
            utils.show(m)
    print("="*80)
    for (mf, c) in d2contents:
        if c not in just1c:
            print(c)
            m = utils.readMutant(mf, f)
            utils.show(m)               
    

if __name__ == '__main__':
    main()
