from __future__ import print_function

import os
import random
import socket
import sys

import universalmutator.mutator as mutator


def main():
    
    languages = {
        ".c": "c",
        ".cpp": "cpp",
        ".c++": "cpp",
        ".py": "python",
        ".java": "java",
        ".swift": "swift",
        ".rs": "rust",
        ".go": "go",
        ".sol": "solidity",
        ".vy": "vyper"}

    cLikeLanguages = [
        "c",
        "java",
        "swift",
        "cpp",
        "c++",
        "rust",
        "solidity",
        "go"]

    sourceFile = sys.argv[1]
    ending = "." + sourceFile.split(".")[-1]

    HOST = '127.0.0.1'
    PORT = 65432

    try:
        language = languages[ending]
    except KeyError:
        language = "none"
    otherRules = []

    if language in cLikeLanguages:
        otherRules.append("c_like.rules")

    if language == "vyper":
        otherRules.append("python.rules")
        otherRules.append("solidity.rules")

    rules = ["universal.rules", language + ".rules"] + otherRules

    if language == "none":
        fuzzRules = ["universal.rules", "c_like.rules", "python.rules", "vyper.rules", "solidity.rules"]
        rules = list(set(fuzzRules + rules))

    (rules, ignoreRules, skipRules) = mutator.compileRules(rules)

    print("STARTING MUTATION SERVER")
    print("WAITING FOR SOURCE INPUTS TO START...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                random.shuffle(rules)
                line = ""
                source = []
                while True:
                    print("TRYING TO READ")
                    data = conn.recv(1).decode('utf-8')
                    print("READ:", data)
                    if not data:
                        print("SOCKET CLOSED, SHUTTING DOWN SERVER")
                        sys.exit(1)
                    line += data
                    if data == "\n":
                        print("READ LINE:", line)
                        if "==END OF MUTANT==" in line:
                            break
                        source.append(line)
                        line = ""
                print("SOURCE:", source)


if __name__ == '__main__':
    main()
