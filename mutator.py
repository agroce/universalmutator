import sys
import re


def mutants(source, rules = ["universal.rules"]):
    rulesText = []

    for ruleFile in rules:
        with open(ruleFile,'r') as file:
            for l in file:
                rulesText.append(l)

    rules = []
    
    for r in rulesText:
        s = r.split(" ==> ")
        lhs = re.compile(s[0])
        if (len(s[1]) > 0) and (s[1][-1] == "\n"):
            rhs = s[1][:-1]
        else:
            rhs = s[1]
        rules.append((lhs,rhs))

    mutants = []
    lineno = 0
    for l in source:
        lineno += 1
        for (lhs,rhs) in rules:
            pos = 0
            p = lhs.search(l,pos)
            while p and (pos < len(l)):
                pos = p.start()+1
                mutant = l[:p.start()] + lhs.sub(rhs,l[p.start():],count=1)
                if mutant[-1] != "\n":
                    mutant += "\n"
                mutants.append((lineno,mutant))
                p = lhs.search(l,pos)    

    return mutants
