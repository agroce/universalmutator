from __future__ import print_function
import argparse


def main():

    parser = argparse.ArgumentParser(prog="intersect_mutants",
                                     description="Write the intersection of two mutant list files to an output file.")
    parser.add_argument("infile1", help="first input mutant list file")
    parser.add_argument("infile2", help="second input mutant list file")
    parser.add_argument("outfile", help="output file for the intersection")
    parsed = parser.parse_args()

    infile1 = parsed.infile1
    infile2 = parsed.infile2
    outfile = parsed.outfile

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
