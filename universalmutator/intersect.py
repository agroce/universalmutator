from __future__ import print_function
import sys


def main():

    args = sys.argv

    if ("--help" in args) or (len(sys.argv) < 2):
        if len(sys.argv) < 2:
            print("ERROR: intersect_mutants requires at least three arguments\n")
        print("USAGE: intersect_mutants <infile1> <infile2> <outfile>")
        sys.exit(0)

    infile1 = sys.argv[1]
    infile2 = sys.argv[2]
    outfile = sys.argv[3]

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
