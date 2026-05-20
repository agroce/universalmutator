from __future__ import print_function

from unittest import TestCase

from universalmutator import mutator


class TestFuncRules(TestCase):
    def test_func_specific_regex_rules_generate_expected_mutants(self):
        source = [
            "int inlineFn(int a) inline {\n",
            "  return a;\n",
            "}\n",
            "int refFn(int a) inline_ref {\n",
            "  return a;\n",
            "}\n",
            "int impureFn() impure {\n",
            "  return 1;\n",
            "}\n",
            "int get_counter() method_id(123) {\n",
            "  return 0;\n",
            "}\n",
            "int get_counter2() method_id {\n",
            "  return 0;\n",
            "}\n",
            "() stdlibOps(cell c, slice s, builder b) impure {\n",
            "  var lr = load_ref(s);\n",
            "  var pr = preload_ref(s);\n",
            "  var ld = load_dict(s);\n",
            "  var pd = preload_dict(s);\n",
            "  var ldi = load_int(s, 8);\n",
            "  var pdi = preload_int(s, 8);\n",
            "  var ldu = load_uint(s, 8);\n",
            "  var pdu = preload_uint(s, 8);\n",
            "  var ldb = load_bits(s, 8);\n",
            "  var pdb = preload_bits(s, 8);\n",
            "  var mpr = s.preload_ref();\n",
            "  var mpd = s.preload_dict();\n",
            "  var mpi = s.preload_int(8);\n",
            "  var mpu = s.preload_uint(8);\n",
            "  var mpb = s.preload_bits(8);\n",
            "  var tlr = s~load_ref();\n",
            "  var tld = s~load_dict();\n",
            "  var lu = s~load_uint(32);\n",
            "  var li = s~load_int(32);\n",
            "  var su = b.store_uint(1, 32);\n",
            "  var si = b.store_int(1, 32);\n",
            "  var tli = s~load_int(8);\n",
            "  var tlu = s~load_uint(8);\n",
            "  var tlb = s~load_bits(8);\n",
            "  var sr = store_ref(b, c);\n",
            "  var sd = store_dict(b, c);\n",
            "  var msr = b.store_ref(c);\n",
            "  var msd = b.store_dict(c);\n",
            "  var sb = skip_bits(s, 8);\n",
            "  var fb = first_bits(s, 8);\n",
            "  var sl = skip_last_bits(s, 8);\n",
            "  var fl = slice_last(s, 8);\n",
            "  var refs = slice_refs(s);\n",
            "  var bits = slice_bits(s);\n",
            "  var empty = slice_empty?(s);\n",
            "  var dempty = slice_data_empty?(s);\n",
            "  var rempty = slice_refs_empty?(s);\n",
            "  var brefs = builder_refs(b);\n",
            "  var bbits = builder_bits(b);\n",
            "  var cn = cell_null?(c);\n",
            "  var de = dict_empty?(c);\n",
            "  var n = now();\n",
            "  var lt = cur_lt();\n",
            "  var blt = block_lt();\n",
            "  var rnd = random();\n",
            "  var seed = get_seed();\n",
            "  var di = idict_get_ref?(c, 256, 0);\n",
            "  var du = udict_set_ref(c, 256, 0, c);\n",
            "  send_raw_message(c, 0);\n",
            "  send_raw_message(c, 1);\n",
            "  send_raw_message(c, 64);\n",
            "  send_raw_message(c, 128);\n",
            "  send_raw_message(c, 1024);\n",
            "  raw_reserve(100, 0);\n",
            "  raw_reserve(100, 2);\n",
            "  raw_reserve_extra(100, c, 0);\n",
            "  var dm = divmod(10, 3);\n",
            "  var md = moddiv(10, 3);\n",
            "  var md2 = a~divmod(b);\n",
            "  var md3 = a~moddiv(b);\n",
            "  var mu1 = muldiv(10, 2, 3);\n",
            "  var mu2 = muldivr(10, 2, 3);\n",
            "  var mu3 = muldivc(10, 2, 3);\n",
            "  var mu4 = muldivmod(10, 2, 3);\n",
            "  accept_message();\n",
            "  commit();\n",
            "  set_code(c);\n",
            "  throw_arg_if(1, 2, 3);\n",
            "  throw_arg_unless(1, 2, 3);\n",
            "}\n",
        ]

        mutants = mutator.mutants_regexp(
            source,
            ruleFiles=["func.rules"],
            ignorePatterns=[],
        )
        mutant_lines = {mutant[1].rstrip() for mutant in mutants}

        self.assertIn("int inlineFn(int a) inline_ref {", mutant_lines)
        self.assertIn("int inlineFn(int a)  {", mutant_lines)
        self.assertIn("int refFn(int a) inline {", mutant_lines)
        self.assertIn("int refFn(int a)  {", mutant_lines)
        self.assertIn("int impureFn()  {", mutant_lines)
        self.assertNotIn("int get_counter() method_id(0) {", mutant_lines)
        self.assertNotIn("int get_counter2() method_id(0) {", mutant_lines)

        self.assertIn("  var pr = s~load_ref();", mutant_lines)
        self.assertIn("  var pd = s~load_dict();", mutant_lines)
        self.assertIn("  var pdi = s~load_int(8);", mutant_lines)
        self.assertIn("  var pdu = s~load_uint(8);", mutant_lines)
        self.assertIn("  var pdb = s~load_bits(8);", mutant_lines)
        self.assertIn("  var mpr = s~load_ref();", mutant_lines)
        self.assertIn("  var mpd = s~load_dict();", mutant_lines)
        self.assertIn("  var mpi = s~load_int(8);", mutant_lines)
        self.assertIn("  var mpu = s~load_uint(8);", mutant_lines)
        self.assertIn("  var mpb = s~load_bits(8);", mutant_lines)
        self.assertIn("  var tlr = s.preload_ref();", mutant_lines)
        self.assertIn("  var tld = s.preload_dict();", mutant_lines)
        self.assertIn("  var lu = s~load_int(32);", mutant_lines)
        self.assertIn("  var lu = s.preload_uint(32);", mutant_lines)
        self.assertIn("  var li = s~load_uint(32);", mutant_lines)
        self.assertIn("  var li = s.preload_int(32);", mutant_lines)
        self.assertIn("  var su = b.store_int(1, 32);", mutant_lines)
        self.assertIn("  var si = b.store_uint(1, 32);", mutant_lines)
        self.assertIn("  var tli = s.preload_int(8);", mutant_lines)
        self.assertIn("  var tlu = s.preload_uint(8);", mutant_lines)
        self.assertIn("  var tlb = s.preload_bits(8);", mutant_lines)
        self.assertIn("  var sr = store_dict(b, c);", mutant_lines)
        self.assertIn("  var sd = store_ref(b, c);", mutant_lines)
        self.assertIn("  var msr = b.store_dict(c);", mutant_lines)
        self.assertIn("  var msd = b.store_ref(c);", mutant_lines)
        self.assertIn("  var sb = first_bits(s, 8);", mutant_lines)
        self.assertIn("  var fb = skip_bits(s, 8);", mutant_lines)
        self.assertIn("  var sl = slice_last(s, 8);", mutant_lines)
        self.assertIn("  var fl = skip_last_bits(s, 8);", mutant_lines)

        self.assertIn("  var refs = slice_bits(s);", mutant_lines)
        self.assertIn("  var bits = slice_refs(s);", mutant_lines)
        self.assertIn("  var empty = slice_refs_empty?(s);", mutant_lines)
        self.assertIn("  var empty = slice_data_empty?(s);", mutant_lines)
        self.assertIn("  var dempty = slice_empty?(s);", mutant_lines)
        self.assertIn("  var dempty = slice_refs_empty?(s);", mutant_lines)
        self.assertIn("  var rempty = slice_empty?(s);", mutant_lines)
        self.assertIn("  var rempty = slice_data_empty?(s);", mutant_lines)
        self.assertIn("  var brefs = builder_bits(b);", mutant_lines)
        self.assertIn("  var bbits = builder_refs(b);", mutant_lines)
        self.assertIn("  var cn = dict_empty?(c);", mutant_lines)
        self.assertIn("  var de = cell_null?(c);", mutant_lines)

        self.assertIn("  var n = cur_lt();", mutant_lines)
        self.assertIn("  var lt = block_lt();", mutant_lines)
        self.assertIn("  var blt = cur_lt();", mutant_lines)
        self.assertIn("  var rnd = get_seed();", mutant_lines)
        self.assertIn("  var seed = random();", mutant_lines)

        self.assertIn("  var di = udict_get_ref?(c, 256, 0);", mutant_lines)
        self.assertIn("  var du = idict_set_ref(c, 256, 0, c);", mutant_lines)

        self.assertIn("  send_raw_message(c, 1);", mutant_lines)
        self.assertIn("  send_raw_message(c, 0);", mutant_lines)
        self.assertIn("  send_raw_message(c, 128);", mutant_lines)
        self.assertIn("  send_raw_message(c, 64);", mutant_lines)
        self.assertIn("  send_raw_message(c, 0);", mutant_lines)

        self.assertIn("  raw_reserve(100, 1);", mutant_lines)
        self.assertIn("  raw_reserve(100, 0);", mutant_lines)
        self.assertIn("  raw_reserve_extra(100, c, 1);", mutant_lines)
        self.assertIn("  var dm = moddiv(10, 3);", mutant_lines)
        self.assertIn("  var md = divmod(10, 3);", mutant_lines)
        self.assertIn("  var md2 = a~moddiv(b);", mutant_lines)
        self.assertIn("  var md3 = a~divmod(b);", mutant_lines)
        self.assertIn("  var mu1 = muldivr(10, 2, 3);", mutant_lines)
        self.assertIn("  var mu2 = muldivc(10, 2, 3);", mutant_lines)
        self.assertIn("  var mu3 = muldiv(10, 2, 3);", mutant_lines)
        self.assertIn("  var mu4 = divmod(10, 2);", mutant_lines)
        self.assertIn("  ;", mutant_lines)
        self.assertIn("  throw_arg_if(1, 2, 3);", mutant_lines)
        self.assertIn("  throw_arg_unless(1, 2, 3);", mutant_lines)

    def test_func_common_regex_rules_generate_expected_mutants(self):
        source = [
            "int coverage_ops(int a, int b, builder bb) {\n",
            "  a += 5;\n",
            "  b -= 6;\n",
            "  a *= 7;\n",
            "  b /= 8;\n",
            "  a &= 1;\n",
            "  b |= 2;\n",
            "  a ^= 3;\n",
            "  a <<= 1;\n",
            "  b >>= 1;\n",
            "  a << 2;\n",
            "  b >> 2;\n",
            "  var tval = true;\n",
            "  var fval = false;\n",
            "  var x = a ^ 1;\n",
            "  var y = a & 1;\n",
            "  var z = a | 1;\n",
            "  if (cond) {\n",
            "  }\n",
            "  ifnot (cond) {\n",
            "    break;\n",
            "  }\n",
            "  while (cond) {\n",
            "    continue;\n",
            "  }\n",
            "  until (cond) {\n",
            "  }\n",
            "  repeat (count) {\n",
            "  }\n",
            "  var diva = a / b;\n",
            "  a /= b;\n",
            "  a %= b;\n",
            "  var moda = a % b;\n",
            "  bb.store_coins(123);\n",
            "  bb.store_int(7, 8);\n",
            "  bb.store_uint(9, 8);\n",
            "  store_uint(bb, 11, 16);\n",
            "  doSomething();\n",
            "  var q = cond ? a : b;\n",
            "  return a;\n",
            "}\n",
        ]

        mutants = mutator.mutants_regexp(
            source,
            ruleFiles=["ton_common.rules", "func.rules"],
            ignorePatterns=[],
        )
        mutant_lines = {mutant[1].rstrip() for mutant in mutants}

        self.assertIn("  a -= 5;", mutant_lines)
        self.assertIn("  b += 6;", mutant_lines)
        self.assertIn("  a |= 1;", mutant_lines)
        self.assertIn("  b &= 2;", mutant_lines)
        self.assertIn("  a >>= 1;", mutant_lines)
        self.assertIn("  a >> 2;", mutant_lines)
        self.assertIn("  var tval = false;", mutant_lines)
        self.assertIn("  var fval = true;", mutant_lines)
        self.assertIn("  var x = a & 1;", mutant_lines)
        self.assertIn("  var y = a ^ 1;", mutant_lines)
        self.assertIn("  if (0) {", mutant_lines)
        self.assertIn("  if (1) {", mutant_lines)
        self.assertIn("  ifnot (0) {", mutant_lines)
        self.assertIn("  ifnot (1) {", mutant_lines)
        self.assertIn("    continue;", mutant_lines)
        self.assertIn("    break;", mutant_lines)
        self.assertIn("  while (false) {", mutant_lines)
        self.assertIn("  until (0) {", mutant_lines)
        self.assertIn("  repeat (0) {", mutant_lines)
        self.assertIn("  var diva = a ~/ b;", mutant_lines)
        self.assertIn("  a ~/= b;", mutant_lines)
        self.assertIn("  a ~%= b;", mutant_lines)
        self.assertIn("  var moda = a ~% b;", mutant_lines)
        self.assertIn("  bb.store_coins(0);", mutant_lines)
        self.assertIn("  bb.store_int(0, 8);", mutant_lines)
        self.assertIn("  bb.store_uint(0, 8);", mutant_lines)
        self.assertIn("  store_uint(bb, 0, 16);", mutant_lines)
        self.assertIn("  ;; doSomething();", mutant_lines)
        self.assertNotIn(";; int coverage_ops(int a, int b, builder bb) {", mutant_lines)
        self.assertNotIn("  ;; if (cond) {", mutant_lines)
        self.assertNotIn("  ;; ifnot (cond) {", mutant_lines)
        self.assertNotIn("  ;; while (cond) {", mutant_lines)
        self.assertNotIn("  ;; repeat (count) {", mutant_lines)
        self.assertNotIn("  ;; var tval = true;", mutant_lines)
        self.assertNotIn("  ;; return a;", mutant_lines)
