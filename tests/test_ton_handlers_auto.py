from __future__ import print_function

import os
import tempfile
from unittest import TestCase, mock

from universalmutator import func_handler
from universalmutator import tact_handler
from universalmutator import tolk_handler


class TestTONAutoHandlers(TestCase):
    def _check_default_handler(
        self,
        handler_module,
        env_var,
        extension,
        source_text,
        mutant_text,
        assertion,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, "contract" + extension)
            mutant_file = os.path.join(temp_dir, ".tmp_mutant" + extension)

            with open(source_file, "w") as f:
                f.write(source_text)
            with open(mutant_file, "w") as f:
                f.write(mutant_text)

            original_text = source_text

            def fake_call(command, shell=False, cwd=None, stderr=None, stdout=None):
                with open(source_file, "r") as f:
                    self.assertEqual(f.read(), mutant_text)
                assertion(command, shell, cwd, temp_dir)
                return 0

            env = os.environ.copy()
            env.pop(env_var, None)

            with mock.patch.dict(os.environ, env, clear=True):
                with mock.patch.object(handler_module.subprocess, "call", side_effect=fake_call):
                    result = handler_module.handler(mutant_file, None, source_file, {})

            self.assertEqual(result, "VALID")
            with open(source_file, "r") as f:
                self.assertEqual(f.read(), original_text)

    def test_tact_default_command_uses_source_directory(self):
        def assertion(command, shell, cwd, temp_dir):
            self.assertTrue(shell)
            self.assertEqual(cwd, temp_dir)
            self.assertEqual(command, "tact --check contract.tact")

        self._check_default_handler(
            tact_handler,
            "UM_TACT_CMD",
            ".tact",
            "fun main() {}\n",
            "fun main() { return; }\n",
            assertion,
        )

    def test_tolk_default_command_uses_source_directory(self):
        def assertion(command, shell, cwd, temp_dir):
            self.assertTrue(shell)
            self.assertEqual(cwd, temp_dir)
            self.assertIn("npx -y @ton/tolk-js --output-json ", command)
            self.assertIn(" contract.tolk", command)

        self._check_default_handler(
            tolk_handler,
            "UM_TOLK_CMD",
            ".tolk",
            'import "helper"\nfun main() {}\n',
            'import "helper"\nfun main() { return; }\n',
            assertion,
        )

    def test_func_default_command_uses_source_directory(self):
        def assertion(command, shell, cwd, temp_dir):
            self.assertTrue(shell)
            self.assertEqual(cwd, temp_dir)
            self.assertIn("npx -y @ton-community/func-js contract.fc --fift ", command)

        self._check_default_handler(
            func_handler,
            "UM_FUNC_CMD",
            ".fc",
            "() main() impure {}\n",
            "() main() impure { throw(1); }\n",
            assertion,
        )
