import os
import tempfile
from unittest import TestCase, mock

from universalmutator import func_handler
from universalmutator import solidity_handler
from universalmutator import tact_handler
from universalmutator import tolk_handler


class TestTempFileCleanup(TestCase):
    def test_ton_handlers_cleanup_temp_files_by_default(self):
        cases = [
            (
                tact_handler,
                ".tact",
                "fun main() {}\n",
                "fun main() { return; }\n",
                [],
            ),
            (
                func_handler,
                ".fc",
                "() main() impure {}\n",
                "() main() impure { throw(1); }\n",
                [(".um.func_output.", ".fif"), (".um.func_log.", "")],
            ),
            (
                tolk_handler,
                ".tolk",
                "fun onInternalMessage(in: InMessage) {}\n",
                "fun onInternalMessage(in: InMessage) { return; }\n",
                [(".um.tolk_output.", ".json"), (".um.tolk_log.", "")],
            ),
        ]

        for handler_module, extension, source_text, mutant_text, extra_outputs in cases:
            with self.subTest(extension=extension):
                with tempfile.TemporaryDirectory() as temp_dir:
                    source_file = os.path.join(temp_dir, "contract" + extension)
                    mutant_file = os.path.join(temp_dir, ".tmp_mutant" + extension)

                    with open(source_file, "w") as f:
                        f.write(source_text)
                    with open(mutant_file, "w") as f:
                        f.write(mutant_text)

                    artifact_prefixes = tuple(item[0] for item in extra_outputs)

                    def fake_call(
                        command,
                        shell=False,
                        cwd=None,
                        stderr=None,
                        stdout=None,
                        artifact_prefixes=artifact_prefixes,
                    ):
                        for artifact_prefix in artifact_prefixes:
                            for token in str(command).split():
                                if artifact_prefix in token:
                                    artifact = token.strip('"')
                                    with open(artifact, "w") as artifact_file:
                                        artifact_file.write("artifact\n")
                                    break
                        return 0

                    env = os.environ.copy()
                    env.pop("UM_KEEP_TEMP", None)
                    original_cwd = os.getcwd()

                    os.chdir(temp_dir)
                    try:
                        with mock.patch.dict(os.environ, env, clear=True):
                            with mock.patch.object(
                                handler_module.subprocess, "call", side_effect=fake_call
                            ):
                                result = handler_module.handler(mutant_file, None, source_file, {})
                    finally:
                        os.chdir(original_cwd)

                    self.assertEqual(result, "VALID")
                    leftovers = [
                        name
                        for name in os.listdir(temp_dir)
                        if name.startswith(".um.") or name.endswith(".um.backup." + str(os.getpid()))
                    ]
                    self.assertEqual(leftovers, [])

    def test_ton_handler_keeps_temp_files_when_requested(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, "contract.fc")
            mutant_file = os.path.join(temp_dir, ".tmp_mutant.fc")

            with open(source_file, "w") as f:
                f.write("() main() impure {}\n")
            with open(mutant_file, "w") as f:
                f.write("() main() impure { throw(1); }\n")

            def fake_call(command, shell=False, cwd=None, stderr=None, stdout=None):
                for token in str(command).split():
                    if ".um.func_output." in token:
                        artifact = token.strip('"')
                        with open(artifact, "w") as artifact_file:
                            artifact_file.write("artifact\n")
                        break
                return 0

            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            try:
                with mock.patch.dict(os.environ, {"UM_KEEP_TEMP": "1"}, clear=True):
                    with mock.patch.object(func_handler.subprocess, "call", side_effect=fake_call):
                        result = func_handler.handler(mutant_file, None, source_file, {})
            finally:
                os.chdir(original_cwd)

            self.assertEqual(result, "VALID")
            leftovers = [name for name in os.listdir(temp_dir) if name.startswith(".um.")]
            self.assertNotEqual(leftovers, [])

    def test_solidity_handler_cleans_backup_and_output_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, "contract.sol")
            mutant_file = os.path.join(temp_dir, ".tmp_mutant.sol")

            with open(source_file, "w") as f:
                f.write("pragma solidity ^0.8.20;\ncontract C { function f() public {} }\n")
            with open(mutant_file, "w") as f:
                f.write("pragma solidity ^0.8.20;\ncontract C { function f() public { revert(); } }\n")

            def fake_call(command, stdout=None, stderr=None):
                stdout.write("EVM assembly:\n")
                stdout.write("tag_1:\n")
                stdout.flush()
                return 0

            env = os.environ.copy()
            env.pop("UM_KEEP_TEMP", None)
            original_cwd = os.getcwd()

            os.chdir(temp_dir)
            try:
                with mock.patch.dict(os.environ, env, clear=True):
                    with mock.patch.object(solidity_handler.subprocess, "call", side_effect=fake_call):
                        result = solidity_handler.handler(mutant_file, None, source_file, {})
            finally:
                os.chdir(original_cwd)

            self.assertEqual(result, "REDUNDANT")
            leftovers = [name for name in os.listdir(temp_dir) if name.startswith(".um.") or ".backup." in name]
            self.assertEqual(leftovers, [])
