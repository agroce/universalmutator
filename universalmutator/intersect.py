from __future__ import print_function
import sys
import argparse


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("infile1",nargs = 1, metavar="<infile1>")

    parser.add_argument("infile2",nargs = 1, metavar="<infile2>")

    parser.add_argument("outfile",nargs = 1, metavar="<outfile>")

    args = parser.parse_args()

    infile1 = args.infile1
    infile2 = args.infile2
    outfile = args.outfile

    infile1_mutants = []
    with open(infile1, 'r') as if1:
        for line in if1:
            infile1_mutants.append(line.split()[0])

    with open(outfile, 'w') as outf:
        with open(infile2, 'r') as if2:
            for line in if2:
                m = line.split()[0]
                if m in infile1_mutants:
                    outf.write(line)


if __name__ == '__main__':
    main()
