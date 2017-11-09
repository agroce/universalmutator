import sys
import re
import pkg_resources

def mutants(source, rules = ["universal.rules"]):
    rulesText = []

    for ruleFile in rules:
        try:
            with pkg_resources.resource_stream('universalmutator', 'static/' + ruleFile) as builtInRule:
                for l in builtInRule:
                    rulesText.append((l,"builtin:"+ruleFile))
        except Exception as e:
            print e
            print "FAILED TO FIND BUILT IN RULE"
            with open(ruleFile,'r') as file:
                for l in file:
                    rulesText.append((l,ruleFile))

    rules = []
    skipRules = []
    
    for (r,ruleSource) in rulesText:
        if r == "\n":
            continue
        if " ==> " not in r:
            if " ==>" in r:
                s = r.split(" ==>")
            else:
                if r[0] == "#": # Don't warn about comments
                    continue
                print "*" * 60
                print "WARNING:"
                print "RULE:",r,"FROM",ruleSource
                print "DOES NOT MATCH EXPECTED FORMAT, AND SO WAS IGNORED"
                print "*" * 60                
                continue # Allow blank lines and comments, just ignore lines without a transformation
        else:
            s = r.split(" ==> ")
        try:
            lhs = re.compile(s[0])
        except:
            print "*"*60
            print "FAILED TO COMPILE RULE:",lhs,"FROM",ruleSource
            print "*"*60            
            continue
        if (len(s[1]) > 0) and (s[1][-1] == "\n"):
            rhs = s[1][:-1]
        else:
            rhs = s[1]
        if rhs != "DO_NOT_MUTATE":
            rules.append((lhs,rhs))
        else:
            skipRules.append(lhs)

    mutants = []
    lineno = 0
    for l in source:
        skipLine = False
        for lhs in skipRules:
            if lhs.search(l):
                skipLine = True
                break
        if skipLine:
            continue
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

def makeMutant(source, mutant, path):
    (lineModified, newCode) = mutant
    with open(path, 'w') as file:
        lineno = 0
        for l in source:
            lineno += 1
            if lineno != lineModified:
                file.write(l)
            else:
                file.write(newCode)
