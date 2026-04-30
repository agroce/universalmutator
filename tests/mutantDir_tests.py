import unittest
import subprocess
import shutil
import os
import stat

test_directory_name = "Test"

# Utility functions to aid in testing
def UtilRemoveTestingDir():
    if os.path.isdir("./"+test_directory_name):
        shutil.rmtree("./"+test_directory_name)

def UtilCreateTestingDir():
    if not os.path.isdir("./"+test_directory_name):
        os.mkdir("./"+test_directory_name)

# execute 'mutate ../examples/foo.py --mutantDir {test_directory_name}', returns true if no errors thrown, false otherwise
def ExecuteMutateWithMutantDir(test_directory):
    try:
        subprocess.run(["mutate", "../examples/foo.py", "--mutantDir", test_directory], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return False

# execute 'mutate ../examples/foo.py --mutantDir {test_directory_name} --legacyMutantDir', returns true if no errors thrown, false otherwise
def ExecuteMutateWithMutantDirAndLegacyMutantDir(test_directory):
    try:
        subprocess.run(["mutate", "../examples/foo.py", "--mutantDir", test_directory, "--legacyMutantDir"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Legacy Error occurred: {e}")
        return False

# Test Cases
class TestMutantDir(unittest.TestCase):
    # When the dir passed into mutantDir does not exist, the program should create a new one
    def test_mutantDir_creatingNewDir(self):
        UtilRemoveTestingDir()
        self.assertEqual(ExecuteMutateWithMutantDir(test_directory_name), True)

    # When the dir passed into mutantDir does exist, the program should NOT create a new one
    def test_mutantDir_alreadyExistingDir(self):
        UtilCreateTestingDir()
        self.assertEqual(ExecuteMutateWithMutantDir(test_directory_name), True)

    # When the dir passed into mutantDir is multiple layers deep (./Parent/Child), and the parent directory does not exist, the program should exit with an error.
    def test_mutantDir_FileNotFoundError(self):
        UtilRemoveTestingDir()
        self.assertEqual(ExecuteMutateWithMutantDir(test_directory_name+"/Test2"), False)

    # When mutate does not have permissions to write into the file passed into --mutantDir, throw a PermissionError and exit.
    def test_mutantDir_PermissionError(self):
        UtilRemoveTestingDir()
        # Create Read Only Dir
        os.mkdir(test_directory_name+"ReadOnly")
        os.chmod(test_directory_name+"ReadOnly", stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

        self.assertEqual(ExecuteMutateWithMutantDir(test_directory_name+"ReadOnly/Test"), False)

        # Remove Read Only Dir
        os.rmdir(test_directory_name+"ReadOnly")

    # When the dir passed into mutantDir does not exist, and the --legacyMutantDir flag is pressent, the program should crash
    def test_legacyMutantDir_DoesIgnoreCheck(self):
        UtilRemoveTestingDir()
        self.assertEqual(ExecuteMutateWithMutantDirAndLegacyMutantDir(test_directory_name), False)

    # When the dir passed into mutantDir does exist, and the --legacyMutantDir flag is pressent, the program should execute normaly
    def test_legactMutantDir_NoCrashWhenDirExists(self):
        UtilCreateTestingDir()
        self.assertEqual(ExecuteMutateWithMutantDirAndLegacyMutantDir(test_directory_name), True)


if __name__ == '__main__':
    # Clean Testing Enviorment
    UtilRemoveTestingDir()

    #Run Tests
    unittest.main(exit=False)

    # Clean Testing Enviorment
    UtilRemoveTestingDir()
