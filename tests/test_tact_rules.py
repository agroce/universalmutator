from __future__ import print_function

from collections import defaultdict
from pathlib import Path
from unittest import TestCase

from universalmutator import mutator


class TestTactRules(TestCase):
    def _mutants(self, source):
        return mutator.mutants_regexp(
            source,
            ruleFiles=["ton_common.rules", "tact.rules"],
            ignorePatterns=[],
        )

    def _mutant_lines(self, source):
        return {mutant[1].rstrip() for mutant in self._mutants(source)}

    def _mutant_lines_by_lineno(self, source):
        by_line = defaultdict(set)
        for lineno, mutant, *_ in self._mutants(source):
            by_line[lineno].add(mutant.rstrip())
        return by_line

    def test_tact_rules_file_has_no_duplicate_rule_lines(self):
        tact_path = Path("universalmutator/static/tact.rules")
        common_path = Path("universalmutator/static/ton_common.rules")

        def rule_lines(rule_path):
            return [
                line.strip()
                for line in rule_path.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            ]

        tact_rule_lines = rule_lines(tact_path)
        common_rule_lines = rule_lines(common_path)

        self.assertEqual(len(tact_rule_lines), len(set(tact_rule_lines)))
        self.assertFalse(set(tact_rule_lines) & set(common_rule_lines))

    def test_tact_rules_do_not_redeclare_shared_ton_arithmetic_families(self):
        text = Path("universalmutator/static/tact.rules").read_text(encoding="utf-8")

        self.assertNotIn(r"(?<!\+)\+(?![\+=]) ==> -", text)
        self.assertNotIn(r"(?<!-)-(?![-=>]) ==> +", text)
        self.assertNotIn(r"\*(?!=) ==> /", text)
        self.assertNotIn(r"/(?!=|\*|/) ==> *", text)

    def test_tact_default_rules_generate_expected_mutants(self):
        source = [
            "fun main() {\n",
            "    a += 5;\n",
            "    b -= 6;\n",
            "    c *= 7;\n",
            "    d /= 8;\n",
            "    e &= 1;\n",
            "    f |= 2;\n",
            "    g ^= 3;\n",
            "    s <<= 1;\n",
            "    t >>= 1;\n",
            "    u << 2;\n",
            "    v >> 2;\n",
            "    var tval = true;\n",
            "    var fval = false;\n",
            "    var x = v ^ 1;\n",
            "    var y = v & 1;\n",
            "    var z = v | 1;\n",
            "    if (cond) {\n",
            "        break;\n",
            "    }\n",
            "    while (cond) {\n",
            "        continue;\n",
            "    }\n",
            "    until (cond) {\n",
            "    }\n",
            "    repeat (count) {\n",
            "    }\n",
            "    var q = cond ? a : b;\n",
            "    throwIf(cond);\n",
            "    throwUnless(cond);\n",
            "    sendRawMessage(msg,\n",
            "        SendDefaultMode);\n",
            "    doSomething();\n",
            "}\n",
        ]

        mutant_lines = self._mutant_lines(source)

        self.assertIn("    a -= 5;", mutant_lines)
        self.assertIn("    b += 6;", mutant_lines)
        self.assertIn("    e |= 1;", mutant_lines)
        self.assertIn("    f &= 2;", mutant_lines)
        self.assertIn("    s >>= 1;", mutant_lines)
        self.assertIn("    u >> 2;", mutant_lines)
        self.assertIn("    var tval = false;", mutant_lines)
        self.assertIn("    var fval = true;", mutant_lines)
        self.assertIn("    var x = v & 1;", mutant_lines)
        self.assertIn("    var y = v ^ 1;", mutant_lines)
        self.assertIn("    if (!(cond)) {", mutant_lines)
        self.assertIn("    if (false) {", mutant_lines)
        self.assertIn("    if (true) {", mutant_lines)
        self.assertIn("        continue;", mutant_lines)
        self.assertIn("        break;", mutant_lines)
        self.assertIn("    while (false) {", mutant_lines)
        self.assertIn("    until (0==1) {", mutant_lines)
        self.assertIn("    repeat (0) {", mutant_lines)
        self.assertIn("    false ?  a  :  b;", mutant_lines)
        self.assertIn("    true ?  a  :  b;", mutant_lines)
        self.assertIn("    throwUnless(cond);", mutant_lines)
        self.assertIn("    throwIf(cond);", mutant_lines)
        self.assertIn("    // doSomething();", mutant_lines)
        self.assertNotIn("// fun main() {", mutant_lines)
        self.assertNotIn("    // if (cond) {", mutant_lines)
        self.assertNotIn("    // while (cond) {", mutant_lines)
        self.assertNotIn("    // var tval = true;", mutant_lines)
        self.assertNotIn("        // SendDefaultMode);", mutant_lines)

    def test_merged_tact_rules_cover_transferred_tact_specific_mutations(self):
        source = [
            "message(0x12345678) Deposit {\n",
            "}\n",
            "    let outgoing = SendParameters { bounce: true, mode: 64, value: 0 };\n",
            "    acceptMessage();\n",
            "    let ownerOk = sender() == self.owner;\n",
            "    let addrOk = myAddress() == target;\n",
            "    external(msg: Slice) {}\n",
            "    inline fun helper() {}\n",
            "    store.set(key, value);\n",
            "    let opt = maybeValue!!;\n",
            "    let amount = payload as uint256;\n",
            "field: Address?;\n",
            "    let incoming = context().value;\n",
            "    if (ctx.value > minValue) {}\n",
            "    if (now() < deadline) {}\n",
            "    let namedDefault = SendDefaultMode;\n",
            "    let namedRemain = SendRemainingValue;\n",
            "    let namedBalance = SendRemainingBalance;\n",
            "    let namedFee = SendOnlyEstimateFee;\n",
            "    let extraFlags = SendPayFwdFeesSeparately | SendBounceIfActionFail | SendDestroyIfZero;\n",
            "    let outgoingFlag1 = SendParameters { bounce: true, mode: 1, value: 0 };\n",
            "    let outgoingFlag16 = SendParameters { bounce: true, mode: 16, value: 0 };\n",
            "    let outgoingFlag32 = SendParameters { bounce: true, mode: 32, value: 0 };\n",
            "    let outgoingFeeOnly = SendParameters { bounce: true, mode: 1024, value: 0 };\n",
            "    let mag = abs(delta);\n",
            "    let round = mulShiftRightRound(x, y, z);\n",
            "    let ceil = mulShiftRightCeil(x, y, z);\n",
            "    let lg = log(amount, 2);\n",
            "    let pw = pow(2, exp);\n",
            "    let lt = curLt();\n",
            "    let blk = blockLt();\n",
            "    let raw = inMsg();\n",
            "    let who = sender();\n",
            "    let me = myAddress();\n",
            "    let balance = myBalance();\n",
            "    let debt = myStorageDue();\n",
            "    let spent = gasConsumed();\n",
            "    let fwd = context().readForwardFee();\n",
            "    let reserveMode = ReserveAllExcept | ReserveBounceIfActionFail;\n",
            "    nativeReserve(amount, 1);\n",
        ]

        mutant_lines = self._mutant_lines(source)

        self.assertIn("message(0xFFFFFFFF) Deposit {", mutant_lines)
        self.assertIn("    let outgoing = SendParameters { bounce: false, mode: 64, value: 0 };", mutant_lines)
        self.assertIn("    let outgoing = SendParameters { bounce: true, mode: 0, value: 0 };", mutant_lines)
        self.assertIn("    let outgoing = SendParameters { bounce: true, mode: 64, value: 1 };", mutant_lines)
        self.assertIn("", mutant_lines)
        self.assertIn("    let ownerOk = sender() != self.owner;", mutant_lines)
        self.assertIn("    let addrOk = myAddress() != target;", mutant_lines)
        self.assertIn("    receive(msg: Slice) {}", mutant_lines)
        self.assertIn("    fun helper() {}", mutant_lines)
        self.assertIn("    store.replace(key, value);", mutant_lines)
        self.assertNotIn("    let opt = maybeValue;", mutant_lines)
        self.assertIn("    let amount = payload as uint128;", mutant_lines)
        self.assertIn("    let amount = payload as int256;", mutant_lines)
        self.assertNotIn("field: Address;", mutant_lines)
        self.assertNotIn("// field: Address?;", mutant_lines)
        self.assertIn("    let incoming = 0;", mutant_lines)
        self.assertIn("    if (0 > minValue) {}", mutant_lines)
        self.assertIn("    if (0 < deadline) {}", mutant_lines)
        self.assertIn("    let namedDefault = SendRemainingValue;", mutant_lines)
        self.assertIn("    let namedRemain = SendDefaultMode;", mutant_lines)
        self.assertIn("    let namedRemain = SendRemainingBalance;", mutant_lines)
        self.assertIn("    let namedBalance = SendDefaultMode;", mutant_lines)
        self.assertIn("    let namedBalance = SendRemainingValue;", mutant_lines)
        self.assertIn("    let namedFee = 0;", mutant_lines)
        self.assertIn("    let extraFlags = 0 | SendBounceIfActionFail | SendDestroyIfZero;", mutant_lines)
        self.assertIn("    let extraFlags = SendPayFwdFeesSeparately | 0 | SendDestroyIfZero;", mutant_lines)
        self.assertIn("    let extraFlags = SendPayFwdFeesSeparately | SendBounceIfActionFail | 0;", mutant_lines)
        self.assertIn("    let outgoingFlag1 = SendParameters { bounce: true, mode: 0, value: 0 };", mutant_lines)
        self.assertIn("    let outgoingFlag16 = SendParameters { bounce: true, mode: 0, value: 0 };", mutant_lines)
        self.assertIn("    let outgoingFlag32 = SendParameters { bounce: true, mode: 0, value: 0 };", mutant_lines)
        self.assertIn("    let outgoingFeeOnly = SendParameters { bounce: true, mode: 0, value: 0 };", mutant_lines)
        self.assertIn("    let mag = sign(delta);", mutant_lines)
        self.assertIn("    let round = mulShiftRight(x, y, z);", mutant_lines)
        self.assertIn("    let round = mulShiftRightCeil(x, y, z);", mutant_lines)
        self.assertIn("    let ceil = mulShiftRight(x, y, z);", mutant_lines)
        self.assertIn("    let ceil = mulShiftRightRound(x, y, z);", mutant_lines)
        self.assertIn("    let lg = log(amount, 10);", mutant_lines)
        self.assertIn("    let pw = pow(10, exp);", mutant_lines)
        self.assertIn("    let lt = blockLt();", mutant_lines)
        self.assertIn("    let blk = curLt();", mutant_lines)
        self.assertIn("    let raw = context().raw;", mutant_lines)
        self.assertIn("    let who = myAddress();", mutant_lines)
        self.assertIn("    let me = sender();", mutant_lines)
        self.assertIn("    let balance = context().value;", mutant_lines)
        self.assertIn("    let debt = gasConsumed();", mutant_lines)
        self.assertIn("    let spent = myStorageDue();", mutant_lines)
        self.assertIn("    let spent = context().readForwardFee();", mutant_lines)
        self.assertIn("    let fwd = gasConsumed();", mutant_lines)
        self.assertIn("    let reserveMode = ReserveExact | ReserveBounceIfActionFail;", mutant_lines)
        self.assertIn("    let reserveMode = ReserveAtMost | ReserveBounceIfActionFail;", mutant_lines)
        self.assertIn("    let reserveMode = ReserveAllExcept | 0;", mutant_lines)
        self.assertIn("    nativeReserve(amount, 0);", mutant_lines)
        self.assertIn("    nativeReserve(amount, 2);", mutant_lines)

    def test_tact_rules_add_compile_safe_tact_families(self):
        source = [
            "let low = min(left, right);\n",
            "let high = max(left, right);\n",
            "let who = context().sender;\n",
            "let reply = sender();\n",
            "let empty = emptyCell();\n",
            "let built = beginCell().endCell();\n",
            "let outgoing = SendParameters { body: null, value: 1, to: sender() };\n",
            "let seeded = SendParameters { body: emptyCell(), value: 1, to: sender() };\n",
        ]

        mutant_lines_by_lineno = self._mutant_lines_by_lineno(source)

        self.assertIn("let low = max(left, right);", mutant_lines_by_lineno[1])
        self.assertIn("let high = min(left, right);", mutant_lines_by_lineno[2])
        self.assertIn("let who = sender();", mutant_lines_by_lineno[3])
        self.assertIn("let reply = context().sender;", mutant_lines_by_lineno[4])
        self.assertIn("let empty = beginCell().endCell();", mutant_lines_by_lineno[5])
        self.assertIn("let built = emptyCell();", mutant_lines_by_lineno[6])
        self.assertIn(
            "let outgoing = SendParameters { body: emptyCell(), value: 1, to: sender() };",
            mutant_lines_by_lineno[7],
        )
        self.assertIn(
            "let seeded = SendParameters { body: null, value: 1, to: sender() };",
            mutant_lines_by_lineno[8],
        )

    def test_foo_tact_fixture_covers_compile_safe_tact_rule_triggers(self):
        source = Path("examples/foo.tact").read_text(encoding="utf-8").splitlines(keepends=True)

        mutant_lines = self._mutant_lines(source)

        self.assertIn("        let minBound = max(msg.amount, forced);", mutant_lines)
        self.assertIn("        let maxBound = min(msg.amount, forced);", mutant_lines)
        self.assertIn("        let ctxSender = sender();", mutant_lines)
        self.assertIn("        let builtCell = emptyCell();", mutant_lines)
        self.assertIn(
            "        let preparedBody = SendParameters { bounce: false, mode: 0, value: 1, to: sender(), body: null };",
            mutant_lines,
        )

    def test_tact_rules_skip_imports_and_comment_only_lines(self):
        source = [
            'import "dep";\n',
            "// full-line comment true && false\n",
            "/* block comment false */\n",
            " * doc comment line true\n",
            "let safe = true; // trailing false\n",
        ]

        mutant_lines_by_lineno = self._mutant_lines_by_lineno(source)

        self.assertNotIn(1, mutant_lines_by_lineno)
        self.assertNotIn(2, mutant_lines_by_lineno)
        self.assertNotIn(3, mutant_lines_by_lineno)
        self.assertNotIn(4, mutant_lines_by_lineno)
        self.assertIn("let safe = false; // trailing false", mutant_lines_by_lineno[5])

    def test_tact_rules_cover_additional_merged_categories(self):
        source = [
            "let eq = a == b;\n",
            "let neq = a != b;\n",
            "let le = a <= b;\n",
            "let ge = a >= b;\n",
            "let lt = a < b;\n",
            "let gt = a > b;\n",
            "let n1 = value == null;\n",
            "let n2 = value != null;\n",
            "let both = left && right;\n",
            "let either = left || right;\n",
            "let sum = a + b;\n",
            "let diff = a - b;\n",
            "let prod = a * b;\n",
            "let ratio = a / b;\n",
            "let low = min(left, right);\n",
            "let high = max(left, right);\n",
            "let outgoing = SendParameters { bounce: false, mode: 128, value: 1 };\n",
            "let flags = SendPayGasSeparately | SendIgnoreErrors | SendRemainingValue | SendRemainingBalance;\n",
            "get fun info() {}\n",
            "extends fun helper() {}\n",
            "extends mutates fun helper2() {}\n",
            "receive(msg: Slice) {}\n",
            "bounced(msg: Slice) {}\n",
            "store.replace(key, value);\n",
            "let width1 = amount as int256;\n",
            "let width2 = amount as coins;\n",
            "field1: Cell?;\n",
            "field2: String?;\n",
            "let acl1 = sender() != owner;\n",
            "let acl2 = self.owner == sender();\n",
            "let acl3 = sender() == self.admin;\n",
            "let acl4 = self.admin != sender();\n",
            "if (context().value > fee) {}\n",
            "if (context().value < cap) {}\n",
            "if (now() > deadline) {}\n",
            "let namedDefault = SendDefaultMode;\n",
            "let namedRemain = SendRemainingValue;\n",
            "let namedBalance = SendRemainingBalance;\n",
            "let namedFee = SendOnlyEstimateFee;\n",
            "let moreFlags = SendPayFwdFeesSeparately | SendBounceIfActionFail | SendDestroyIfZero;\n",
            "let outgoingFlag1 = SendParameters { bounce: false, mode: 1, value: 1 };\n",
            "let outgoingFlag16 = SendParameters { bounce: false, mode: 16, value: 1 };\n",
            "let outgoingFlag32 = SendParameters { bounce: false, mode: 32, value: 1 };\n",
            "let outgoingFeeOnly = SendParameters { bounce: false, mode: 1024, value: 1 };\n",
            "let mag = sign(delta);\n",
            "let baseRound = mulShiftRight(x, y, z);\n",
            "let lg = log(amount, 10);\n",
            "let pw = pow(10, exp);\n",
            "let lt = curLt();\n",
            "let blk = blockLt();\n",
            "let raw = inMsg();\n",
            "let who = sender();\n",
            "let me = myAddress();\n",
            "let balance = myBalance();\n",
            "let debt = myStorageDue();\n",
            "let spent = gasConsumed();\n",
            "let fwd = context().readForwardFee();\n",
            "let reserveMode = ReserveAllExcept | ReserveBounceIfActionFail;\n",
            "nativeReserve(amount, 1);\n",
        ]

        mutant_lines_by_lineno = self._mutant_lines_by_lineno(source)

        self.assertIn("let eq = a != b;", mutant_lines_by_lineno[1])
        self.assertIn("let neq = a == b;", mutant_lines_by_lineno[2])
        self.assertIn("let le = a < b;", mutant_lines_by_lineno[3])
        self.assertIn("let ge = a > b;", mutant_lines_by_lineno[4])
        self.assertIn("let lt = a <= b;", mutant_lines_by_lineno[5])
        self.assertIn("let gt = a >= b;", mutant_lines_by_lineno[6])
        self.assertIn("let n1 = value != null;", mutant_lines_by_lineno[7])
        self.assertIn("let n2 = value == null;", mutant_lines_by_lineno[8])
        self.assertIn("let sum = a - b;", mutant_lines_by_lineno[11])
        self.assertIn("let diff = a + b;", mutant_lines_by_lineno[12])
        self.assertIn("let prod = a / b;", mutant_lines_by_lineno[13])
        self.assertIn("let ratio = a * b;", mutant_lines_by_lineno[14])
        self.assertIn("let outgoing = SendParameters { bounce: true, mode: 128, value: 1 };", mutant_lines_by_lineno[17])
        self.assertIn("let outgoing = SendParameters { bounce: false, mode: 0, value: 1 };", mutant_lines_by_lineno[17])
        self.assertIn("let outgoing = SendParameters { bounce: false, mode: 64, value: 1 };", mutant_lines_by_lineno[17])
        self.assertIn("let outgoing = SendParameters { bounce: false, mode: 128, value: 0 };", mutant_lines_by_lineno[17])
        self.assertIn("let flags = 0 | SendIgnoreErrors | SendRemainingValue | SendRemainingBalance;", mutant_lines_by_lineno[18])
        self.assertIn("let flags = SendPayGasSeparately | 0 | SendRemainingValue | SendRemainingBalance;", mutant_lines_by_lineno[18])
        self.assertIn("let flags = SendPayGasSeparately | SendIgnoreErrors | 0 | SendRemainingBalance;", mutant_lines_by_lineno[18])
        self.assertIn("let flags = SendPayGasSeparately | SendIgnoreErrors | SendRemainingValue | 0;", mutant_lines_by_lineno[18])
        self.assertIn("fun info() {}", mutant_lines_by_lineno[19])
        self.assertNotIn("fun helper() {}", mutant_lines_by_lineno.get(20, set()))
        self.assertNotIn("mutates fun helper2() {}", mutant_lines_by_lineno.get(21, set()))
        self.assertIn("external(msg: Slice) {}", mutant_lines_by_lineno[22])
        self.assertNotIn("receive(msg: Slice) {}", mutant_lines_by_lineno.get(23, set()))
        self.assertIn("store.set(key, value);", mutant_lines_by_lineno[24])
        self.assertIn("let width1 = amount as int128;", mutant_lines_by_lineno[25])
        self.assertIn("let width1 = amount as uint256;", mutant_lines_by_lineno[25])
        self.assertIn("let width2 = amount as uint64;", mutant_lines_by_lineno[26])
        self.assertNotIn("field1: Cell;", mutant_lines_by_lineno.get(27, set()))
        self.assertNotIn("field2: String;", mutant_lines_by_lineno.get(28, set()))
        self.assertIn("let acl1 = sender() == owner;", mutant_lines_by_lineno[29])
        self.assertIn("let acl2 = self.owner != sender();", mutant_lines_by_lineno[30])
        self.assertIn("let acl3 = sender() != self.admin;", mutant_lines_by_lineno[31])
        self.assertIn("let acl4 = self.admin == sender();", mutant_lines_by_lineno[32])
        self.assertIn("if (0 > fee) {}", mutant_lines_by_lineno[33])
        self.assertIn("if (0 < cap) {}", mutant_lines_by_lineno[34])
        self.assertIn("if (0 > deadline) {}", mutant_lines_by_lineno[35])
        self.assertIn("let namedDefault = SendRemainingValue;", mutant_lines_by_lineno[36])
        self.assertIn("let namedRemain = SendDefaultMode;", mutant_lines_by_lineno[37])
        self.assertIn("let namedRemain = SendRemainingBalance;", mutant_lines_by_lineno[37])
        self.assertIn("let namedBalance = SendDefaultMode;", mutant_lines_by_lineno[38])
        self.assertIn("let namedBalance = SendRemainingValue;", mutant_lines_by_lineno[38])
        self.assertIn("let namedFee = 0;", mutant_lines_by_lineno[39])
        self.assertIn("let moreFlags = 0 | SendBounceIfActionFail | SendDestroyIfZero;", mutant_lines_by_lineno[40])
        self.assertIn("let moreFlags = SendPayFwdFeesSeparately | 0 | SendDestroyIfZero;", mutant_lines_by_lineno[40])
        self.assertIn("let moreFlags = SendPayFwdFeesSeparately | SendBounceIfActionFail | 0;", mutant_lines_by_lineno[40])
        self.assertIn("let outgoingFlag1 = SendParameters { bounce: false, mode: 0, value: 1 };", mutant_lines_by_lineno[41])
        self.assertIn("let outgoingFlag16 = SendParameters { bounce: false, mode: 0, value: 1 };", mutant_lines_by_lineno[42])
        self.assertIn("let outgoingFlag32 = SendParameters { bounce: false, mode: 0, value: 1 };", mutant_lines_by_lineno[43])
        self.assertIn("let outgoingFeeOnly = SendParameters { bounce: false, mode: 0, value: 1 };", mutant_lines_by_lineno[44])
        self.assertIn("let mag = abs(delta);", mutant_lines_by_lineno[45])
        self.assertIn("let baseRound = mulShiftRightRound(x, y, z);", mutant_lines_by_lineno[46])
        self.assertIn("let baseRound = mulShiftRightCeil(x, y, z);", mutant_lines_by_lineno[46])
        self.assertIn("let lg = log(amount, 2);", mutant_lines_by_lineno[47])
        self.assertIn("let pw = pow(2, exp);", mutant_lines_by_lineno[48])
        self.assertIn("let lt = blockLt();", mutant_lines_by_lineno[49])
        self.assertIn("let blk = curLt();", mutant_lines_by_lineno[50])
        self.assertIn("let raw = context().raw;", mutant_lines_by_lineno[51])
        self.assertIn("let who = myAddress();", mutant_lines_by_lineno[52])
        self.assertIn("let me = sender();", mutant_lines_by_lineno[53])
        self.assertIn("let balance = context().value;", mutant_lines_by_lineno[54])
        self.assertIn("let debt = gasConsumed();", mutant_lines_by_lineno[55])
        self.assertIn("let spent = myStorageDue();", mutant_lines_by_lineno[56])
        self.assertIn("let spent = context().readForwardFee();", mutant_lines_by_lineno[56])
        self.assertIn("let fwd = gasConsumed();", mutant_lines_by_lineno[57])
        self.assertIn("let reserveMode = ReserveExact | ReserveBounceIfActionFail;", mutant_lines_by_lineno[58])
        self.assertIn("let reserveMode = ReserveAtMost | ReserveBounceIfActionFail;", mutant_lines_by_lineno[58])
        self.assertIn("let reserveMode = ReserveAllExcept | 0;", mutant_lines_by_lineno[58])
        self.assertIn("nativeReserve(amount, 0);", mutant_lines_by_lineno[59])
        self.assertIn("nativeReserve(amount, 2);", mutant_lines_by_lineno[59])
