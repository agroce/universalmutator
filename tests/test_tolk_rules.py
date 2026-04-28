from __future__ import print_function

from unittest import TestCase

from universalmutator import mutator


class TestTolkRules(TestCase):
    def test_tolk_specific_regex_rules_generate_expected_mutants(self):
        source = [
            "struct (0x12345678) CounterIncrement {\n",
            "    incBy: uint32\n",
            "    decBy: int32\n",
            "}\n",
            "struct (0x01) ShortPrefix {\n",
            "    value: uint8\n",
            "}\n",
            "struct AuctionConfig {\n",
            "    ownerAddress: address? = null\n",
            "    minBid: coins = 0\n",
            "}\n",
            "fun CounterIncrement.bump(mutate self): self {\n",
            "    return self;\n",
            "}\n",
            "@inline\n",
            "fun inlineFn(a: int, delta: int = 1): int {\n",
            "    return a + delta;\n",
            "}\n",
            "@noinline\n",
            "fun noinlineFn(a: int): int {\n",
            "    return a;\n",
            "}\n",
            "@inline_ref\n",
            "fun refFn(a: int): int {\n",
            "    return a;\n",
            "}\n",
            "@pure\n",
            "@method_id(123)\n",
            "fun taggedFn(): int {\n",
            "    return 1;\n",
            "}\n",
            "fun helper(mutate cs: slice, mutate amount: int, target: Cell<address>?, body: slice) {\n",
            "    assert (amount > 0) throw ERR;\n",
            "    var parsed = target!;\n",
            "    var casted = parsed as address;\n",
            "    var msg = Allowed.fromSlice(body, { throwIfOpcodeDoesNotMatch: ERR_INVALID_OP });\n",
            "    return (cs, amount, casted, msg);\n",
            "}\n",
            "get fun currentCounter(): int {\n",
            "    return 0;\n",
            "}\n",
            "fun castNumber(flag: bool, a: uint64, b: int64): int {\n",
            "    var x = a as uint32;\n",
            "    var y = b as int32;\n",
            "    var z: varuint16 = 0;\n",
            "    return x + y + z;\n",
            "}\n",
            "fun stdlibOps(c: cell, s: slice) {\n",
            "    var nowTs = blockchain.now();\n",
            "    var lt = blockchain.logicalTime();\n",
            "    var blockLt = blockchain.currentBlockLogicalTime();\n",
            "    var csz = c.calculateSizeStrict();\n",
            "    var ssz = s.calculateSize();\n",
            "    var fwd = calculateForwardFee(0, 100, 1);\n",
            "    var fwdNoLump = calculateForwardFeeWithoutLumpPrice(0, 100, 1);\n",
            "    var gas = calculateGasFee(0, 100);\n",
            "    var gasNoFlat = calculateGasFeeWithoutFlatPrice(0, 100);\n",
            "    var rnd = random.uint256();\n",
            "    var seed = random.getSeed();\n",
            "    acceptExternalMessage();\n",
            "    commitContractDataAndActions();\n",
            "}\n",
            "fun sendModes(msg: cell) {\n",
            "    notify.send(SEND_MODE_REGULAR);\n",
            "    deploy.send(0);\n",
            "    sendRawMessage(msg, 0);\n",
            "    sendRawMessage(msg, SEND_MODE_IGNORE_ERRORS | SEND_MODE_CARRY_ALL_REMAINING_MESSAGE_VALUE);\n",
            "    sendRawMessage(msg, SEND_MODE_PAY_FEES_SEPARATELY | SEND_MODE_BOUNCE_ON_ACTION_FAIL);\n",
            "    sendRawMessage(msg, SEND_MODE_CARRY_ALL_BALANCE);\n",
            "    reserveToncoinsOnBalance(ton(\"0.01\"), RESERVE_MODE_AT_MOST);\n",
            "    reserveToncoinsOnBalance(ton(\"0.01\"), RESERVE_MODE_EXACT_AMOUNT);\n",
            "}\n",
            "fun stringsOps(metadataUri: string) {\n",
            "    var offchain = metadataUri.prefixWith00();\n",
            "    var regular = metadataUri.prefixWith01();\n",
            "    val crc = \"some_str\".crc32();\n",
            "    val crcSmall = \"some_str\".crc16();\n",
            "    val hash = \"some_crypto_key\".sha256();\n",
            "    val minihash = \"some_crypto_key\".sha256_32();\n",
            "    val oldCrc = stringCrc32(\"legacy\");\n",
            "    val oldSmall = stringCrc16(\"legacy\");\n",
            "    val oldHash = stringSha256(\"legacy\");\n",
            "    val oldMinihash = stringSha256_32(\"legacy\");\n",
            "}\n",
            "fun classify(value: CounterIncrement | null, body: slice) {\n",
            "    val msg = lazy AllowedMessage.fromSlice(body);\n",
            "    if (value is CounterIncrement) {\n",
                "        var noBounce = BounceMode.NoBounce;\n",
            "        var rich = BounceMode.RichBounce;\n",
            "        var root = BounceMode.RichBounceOnlyRootCell;\n",
            "        var shortBody = BounceMode.Only256BitsOfBody;\n",
            "    }\n",
            "    if (value !is CounterIncrement) {\n",
            "        return;\n",
            "    }\n",
            "}\n",
            "fun onBouncedMessage(in: InMessageBounced) {\n",
            "}\n",
            "fun onInternalMessage(in: InMessage) {\n",
            "}\n",
        ]

        mutants = mutator.mutants_regexp(
            source,
            ruleFiles=["ton_common.rules", "tolk.rules"],
            ignorePatterns=[],
        )
        mutant_lines = {mutant[1].rstrip() for mutant in mutants}

        self.assertIn("struct (0x00000000) CounterIncrement {", mutant_lines)
        self.assertIn("struct (0xFFFFFFFF) CounterIncrement {", mutant_lines)
        self.assertIn("struct (0x00000000) ShortPrefix {", mutant_lines)
        self.assertIn("struct (0xFFFFFFFF) ShortPrefix {", mutant_lines)
        self.assertIn("    ownerAddress: address?", mutant_lines)
        self.assertIn("    minBid: coins", mutant_lines)
        self.assertIn("    incBy: int32", mutant_lines)
        self.assertIn("    decBy: uint32", mutant_lines)
        self.assertIn("fun CounterIncrement.bump(self): self {", mutant_lines)
        self.assertIn("@noinline", mutant_lines)
        self.assertIn("@inline", mutant_lines)
        self.assertIn("fun inlineFn(a: int, delta: int): int {", mutant_lines)
        self.assertIn("fun helper(cs: slice, mutate amount: int, target: Cell<address>?, body: slice) {", mutant_lines)
        self.assertIn("fun helper(mutate cs: slice, amount: int, target: Cell<address>?, body: slice) {", mutant_lines)
        self.assertIn("    var parsed = target;", mutant_lines)
        self.assertIn("    var msg = Allowed.fromSlice(body, { throwIfOpcodeDoesNotMatch: 63 });", mutant_lines)
        self.assertIn("fun currentCounter(): int {", mutant_lines)
        self.assertIn("    var x = a as int32;", mutant_lines)
        self.assertIn("    var y = b as uint32;", mutant_lines)
        self.assertIn("    var z: varint16 = 0;", mutant_lines)
        self.assertIn("    var nowTs = blockchain.logicalTime();", mutant_lines)
        self.assertIn("    var lt = blockchain.currentBlockLogicalTime();", mutant_lines)
        self.assertIn("    var blockLt = blockchain.logicalTime();", mutant_lines)
        self.assertIn("    var csz = c.calculateSize();", mutant_lines)
        self.assertIn("    var ssz = s.calculateSizeStrict();", mutant_lines)
        self.assertIn("    var fwd = calculateForwardFeeWithoutLumpPrice(0, 100, 1);", mutant_lines)
        self.assertIn("    var fwdNoLump = calculateForwardFee(0, 100, 1);", mutant_lines)
        self.assertIn("    var gas = calculateGasFeeWithoutFlatPrice(0, 100);", mutant_lines)
        self.assertIn("    var gasNoFlat = calculateGasFee(0, 100);", mutant_lines)
        self.assertIn("    var rnd = random.getSeed();", mutant_lines)
        self.assertIn("    var seed = random.uint256();", mutant_lines)
        self.assertIn("    commitContractDataAndActions();", mutant_lines)
        self.assertIn("    acceptExternalMessage();", mutant_lines)
        self.assertIn("    notify.send(SEND_MODE_CARRY_ALL_REMAINING_MESSAGE_VALUE);", mutant_lines)
        self.assertIn("    deploy.send(64);", mutant_lines)
        self.assertIn("    sendRawMessage(msg, 64);", mutant_lines)
        self.assertIn("    sendRawMessage(msg, 0 | SEND_MODE_CARRY_ALL_REMAINING_MESSAGE_VALUE);", mutant_lines)
        self.assertIn("    sendRawMessage(msg, SEND_MODE_IGNORE_ERRORS | SEND_MODE_CARRY_ALL_BALANCE);", mutant_lines)
        self.assertIn(
            "    sendRawMessage(msg, SEND_MODE_IGNORE_ERRORS | SEND_MODE_REGULAR);",
            mutant_lines,
        )
        self.assertIn("    sendRawMessage(msg, 0 | SEND_MODE_BOUNCE_ON_ACTION_FAIL);", mutant_lines)
        self.assertIn("    sendRawMessage(msg, SEND_MODE_PAY_FEES_SEPARATELY | 0);", mutant_lines)
        self.assertIn("    sendRawMessage(msg, SEND_MODE_CARRY_ALL_REMAINING_MESSAGE_VALUE);", mutant_lines)
        self.assertIn("    sendRawMessage(msg, SEND_MODE_REGULAR);", mutant_lines)
        self.assertIn('    reserveToncoinsOnBalance(ton("0.01"), RESERVE_MODE_EXACT_AMOUNT);', mutant_lines)
        self.assertIn('    reserveToncoinsOnBalance(ton("0.01"), RESERVE_MODE_AT_MOST);', mutant_lines)
        self.assertIn('    val oldCrc = stringCrc16("legacy");', mutant_lines)
        self.assertIn('    val oldSmall = stringCrc32("legacy");', mutant_lines)
        self.assertIn('    val oldHash = stringSha256_32("legacy");', mutant_lines)
        self.assertIn('    val oldMinihash = stringSha256("legacy");', mutant_lines)
        self.assertIn("    val msg = AllowedMessage.fromSlice(body);", mutant_lines)
        self.assertIn("    if (value !is CounterIncrement) {", mutant_lines)
        self.assertIn("    if (value is CounterIncrement) {", mutant_lines)
        self.assertIn("        var noBounce = BounceMode.RichBounce;", mutant_lines)
        self.assertIn("        var root = BounceMode.RichBounce;", mutant_lines)
        self.assertIn("        var shortBody = BounceMode.RichBounce;", mutant_lines)

    def test_tolk_common_regex_rules_generate_expected_mutants(self):
        source = [
            "fun coverageOps() {\n",
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
            "    sendRawMessage(msg,\n",
            "        SEND_MODE_REGULAR);\n",
            "    doSomething();\n",
            "}\n",
        ]

        mutants = mutator.mutants_regexp(
            source,
            ruleFiles=["ton_common.rules", "tolk.rules"],
            ignorePatterns=[],
        )
        mutant_lines = {mutant[1].rstrip() for mutant in mutants}

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
        self.assertIn("    // doSomething();", mutant_lines)
        self.assertNotIn("// fun coverageOps() {", mutant_lines)
        self.assertNotIn("    // if (cond) {", mutant_lines)
        self.assertNotIn("    // while (cond) {", mutant_lines)
        self.assertNotIn("    // var tval = true;", mutant_lines)
        self.assertNotIn("        // SEND_MODE_REGULAR);", mutant_lines)
