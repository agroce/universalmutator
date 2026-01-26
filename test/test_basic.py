import subprocess

def test_record_replay():
    r = subprocess.call(["gcc -o toy test/toy.c"], shell=True)
    assert r == 0

    with open("out1.txt", 'w') as f:
        r = subprocess.call(["mkdir mutants; rm mutants/*; muttfuzz \"./toy\" toy --score --avoid_repeats --stop_on_repeat --repeat_retries 2000 --save_results analysis.csv --save_mutants mutants"], shell=True, stdout=f, stderr=f)
    with open("out1.txt", 'r') as f:
        contents = f.read()
    print(contents)
    assert r == 0
    assert "FINAL MUTATION SCORE OVER 14 EXECUTED MUTANTS: 57.14%" in contents

    with open("out2.txt", 'w') as f:
        r = subprocess.call(["muttfuzz \"./toy\" toy --score --avoid_repeats --stop_on_repeat --save_results s_analysis.csv --use_saved_mutants mutants"], shell=True, stdout=f, stderr=f)
    with open("out2.txt", 'r') as f:
        contents = f.read()
    print(contents)
    assert r == 0
    assert "FINAL MUTATION SCORE OVER 14 EXECUTED MUTANTS: 57.14%" in contents
