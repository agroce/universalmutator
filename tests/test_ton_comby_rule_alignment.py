from pathlib import Path
from unittest import TestCase

from universalmutator import mutator


class TestTonCombyRuleAlignment(TestCase):
    def _read_comby_rules(self, filename):
        mutator.parseRules([filename], comby=True)
        return (Path("universalmutator/comby") / filename).read_text(encoding="utf-8")

    def test_ton_common_comby_rules_cover_shared_ton_defaults(self):
        text = self._read_comby_rules("ton_common.rules")

        self.assertIn(":[lhs~[^,\\n]+] == :[rhs~[^,\\n]+] ==> :[lhs] != :[rhs]", text)
        self.assertIn(
            ":[lhs~(?!.*(?:\\bis\\b|!is\\b)).*] && :[rhs~(?!.*(?:\\bis\\b|!is\\b)).*] ==> :[lhs] || :[rhs]",
            text,
        )
        self.assertIn(
            ":[lhs~(?!.*(?:\\bis\\b|!is\\b)).*] || :[rhs~(?!.*(?:\\bis\\b|!is\\b)).*] ==> :[lhs] && :[rhs]",
            text,
        )
        self.assertNotIn("if (:[cond]) ==> if (!(:[cond]))", text)
        self.assertIn("while (:[cond]) ==> while (false)", text)
        self.assertIn("break; ==> continue;", text)
        self.assertIn(":[lhs]+=:[rhs] ==> :[lhs]-=:[rhs]", text)
        self.assertIn(":[lhs~.*[^~^]\\s*]/=:[rhs] ==> :[lhs]+=:[rhs]", text)
        self.assertNotIn(":[lhs]/=:[rhs] ==> :[lhs]+=:[rhs]", text)
        self.assertIn(":[lhs]<<:[rhs] ==> :[lhs]>>:[rhs]", text)

    def test_tact_comby_rules_track_added_static_families(self):
        text = self._read_comby_rules("tact.rules")

        self.assertIn("if (:[cond]) ==> if (!(:[cond]))", text)
        self.assertIn("if (:[cond]) ==> if (false)", text)
        self.assertIn("if (:[cond]) ==> if (true)", text)
        self.assertIn(":[lhs~.*\\s]^:[rhs~.*] ==> :[lhs]&:[rhs]", text)
        self.assertIn("until (:[cond]) ==> until (0==1)", text)
        self.assertIn("repeat (:[count]) ==> repeat (0)", text)
        self.assertIn("throw(:[code~\\d+]); ==> throw(0);", text)
        self.assertIn("message(0x:[opcode~[0-9a-fA-F]{8}]) ==> message(0xFFFFFFFF)", text)
        self.assertIn("randomInt() ==> getSeed()", text)
        self.assertIn("setSeed(:[seed]) ==> nativeRandomize(:[seed])", text)
        self.assertIn("nativeRandomInterval(:[max]) ==> random(0, :[max])", text)
        self.assertIn("min(:[x], :[y]) ==> max(:[x], :[y])", text)
        self.assertIn("max(:[x], :[y]) ==> min(:[x], :[y])", text)
        self.assertIn("context().sender ==> sender()", text)
        self.assertIn("sender() ==> context().sender", text)
        self.assertIn("emptyCell() ==> beginCell().endCell()", text)
        self.assertIn("beginCell().endCell() ==> emptyCell()", text)
        self.assertIn("body: null ==> body: emptyCell()", text)
        self.assertIn("body: emptyCell() ==> body: null", text)
        self.assertNotIn(":[expr]!! ==> :[expr]", text)
        self.assertNotIn(":[name]: Address?; ==> :[name]: Address;", text)
        self.assertNotIn("extends mutates fun :[rest] ==> mutates fun :[rest]", text)
        self.assertNotIn("extends fun :[rest] ==> fun :[rest]", text)
        self.assertNotIn("bounced(:[args]) ==> receive(:[args])", text)

        self.assertNotIn("true ==> false", text)
        self.assertNotIn(":[lhs]+=:[rhs] ==> :[lhs]-=:[rhs]", text)
        self.assertNotIn(":[lhs]&=:[rhs] ==> :[lhs]|=:[rhs]", text)
        self.assertNotIn(":[lhs]<<:[rhs] ==> :[lhs]>>:[rhs]", text)
        self.assertNotIn("while (:[cond]) ==> while (0==1)", text)
        self.assertNotIn("while (:[cond]) ==> while (false)", text)
        self.assertNotIn("break; ==> continue;", text)

    def test_func_comby_rules_drop_comby_only_block_comment_guard(self):
        text = self._read_comby_rules("func.rules")

        self.assertIn("Line-anchored comment replacement stays regex-only", text)
        self.assertNotIn(":[lhs]+=:[rhs] ==> :[lhs]-=:[rhs]", text)
        self.assertNotIn(":[lhs]&=:[rhs] ==> :[lhs]|=:[rhs]", text)
        self.assertIn(r":[a~\w+] ^ :[b~\w+] ==> :[a] & :[b]", text)
        self.assertIn("if (:[cond]) ==> if (0)", text)
        self.assertIn("if (:[cond]) ==> if (1)", text)
        self.assertIn("ifnot (:[cond]) ==> ifnot (0)", text)
        self.assertIn("until (:[cond]) ==> until (0)", text)
        self.assertIn(".store_uint(:[x], :[len]) ==> .store_int(:[x], :[len])", text)
        self.assertIn("preload_uint(:[s~[A-Za-z_][A-Za-z0-9_]*], :[len]) ==> :[s]~load_uint(:[len])", text)
        self.assertIn(":[s~[A-Za-z_][A-Za-z0-9_]*]~load_uint(:[len]) ==> :[s].preload_uint(:[len])", text)
        self.assertIn("skip_bits(:[s], :[len]) ==> first_bits(:[s], :[len])", text)
        self.assertIn("store_ref(:[b], :[c]) ==> store_dict(:[b], :[c])", text)
        self.assertIn("throw_unless(:[err], :[lhs] == :[rhs]) ==> throw_unless(:[err], :[lhs] != :[rhs])", text)
        self.assertIn(":[lhs~.*[^~^]\\s*]/=:[rhs] ==> :[lhs]~/=:[rhs]", text)
        self.assertNotIn("method_id(:[id]) ==> method_id(0)", text)
        self.assertNotIn("break; ==> continue;", text)
        self.assertNotIn("while (:[cond]) ==> while (0==1)", text)
        self.assertNotIn("{-:[comment]-} ==> DO_NOT_MUTATE", text)
        self.assertIn("if(:[cond]) ==> if(0)", text)
        self.assertIn("inline ==> inline_ref", text)
        self.assertNotIn("load_ref(:[s]) ==> preload_ref(:[s])", text)
        self.assertNotIn(".preload_uint(:[len]) ==> .load_uint(:[len])", text)
        self.assertNotIn("\nat(:[t], :[i]) ==> tuple_at(:[t], :[i])\n", text)
        self.assertNotIn("\nint_at(:[t], :[i]) ==> cell_at(:[t], :[i])\n", text)

    def test_tolk_comby_rules_remove_unpaired_comby_only_mutations(self):
        text = self._read_comby_rules("tolk.rules")

        self.assertIn("Line-anchored comment replacement stays regex-only", text)
        self.assertNotIn(":[lhs]+=:[rhs] ==> :[lhs]-=:[rhs]", text)
        self.assertNotIn(":[lhs]&=:[rhs] ==> :[lhs]|=:[rhs]", text)
        self.assertIn("if (:[cond]) ==> if (!(:[cond]))", text)
        self.assertIn("if (:[cond]) ==> if (false)", text)
        self.assertIn("if (:[cond]) ==> if (true)", text)
        self.assertIn("assert (:[cond]) throw :[err]; ==> // assert (:[cond]) throw :[err];", text)
        self.assertIn("assert (:[cond]) throw :[err]; ==> assert (!(:[cond])) throw :[err];", text)
        self.assertIn("value: :[expr~[a-zA-Z0-9_.]+] ==> value: 0", text)
        self.assertIn("assert (:[lhs] == :[rhs]) throw :[err] ==> assert (:[lhs] != :[rhs]) throw :[err]", text)
        self.assertIn("if (:[lhs] == :[rhs]) ==> if (:[lhs] != :[rhs])", text)
        self.assertNotIn("while (:[cond]) ==> while (0==1)", text)
        self.assertNotIn("break; ==> continue;", text)
        self.assertIn("calculateSizeStrict(:[args]) ==> calculateSize(:[args])", text)
        self.assertIn(":[recv~(?!\\s*fun\\b).*].sendAndEstimateFee(:[args]) ==> :[recv].estimateFeeWithoutSending(:[args])", text)
        self.assertIn(":[msg].send(:[mode]) ==> :[msg].sendAndEstimateFee(:[mode])", text)
        self.assertIn(
            "reserveToncoinsOnBalance(:[amount], :[mode]) ==> reserveExtraCurrenciesOnBalance(:[amount], null, :[mode])",
            text,
        )
        self.assertIn(
            "reserveExtraCurrenciesOnBalance(:[amount], :[extra], :[mode]) ==> reserveToncoinsOnBalance(:[amount], :[mode])",
            text,
        )
        self.assertIn(":[recv].storeRef(:[args]) ==> :[recv].storeMaybeRef(:[args])", text)
        self.assertIn("assertEndAfterReading: true ==> assertEndAfterReading: false", text)
        self.assertIn("assertEndAfterReading: false ==> assertEndAfterReading: true", text)
        self.assertIn(
            "struct (:[opcode~(?:0x[0-9A-Fa-f]+|0b[01]+)]) :[name] { ==> struct (0x00000000) :[name] {",
            text,
        )
        self.assertIn("throw :[err]; ==> ", text)
        self.assertIn(":[obj].save(:[args]); ==> ", text)
        self.assertIn("contract.setData(:[args]); ==> ", text)
        self.assertIn("acceptExternalMessage(); ==> ", text)
        self.assertIn("commitContractDataAndActions(); ==> ", text)
        self.assertIn("contract.setCodePostponed(:[args]); ==> ", text)
        self.assertIn(":[lhs] *= :[rhs] ==> :[lhs] %= :[rhs]", text)
        self.assertIn(":[lhs] %= :[rhs] ==> :[lhs] *= :[rhs]", text)
        self.assertNotIn("//:[comment] ==> DO_NOT_MUTATE", text)
        self.assertNotIn("@method_id(:[id]) ==> @method_id(0)", text)
        self.assertNotIn("mutate self ==> self", text)
        self.assertNotIn(":[lhs] is :[rhs] ==> :[lhs] !is :[rhs]", text)
        self.assertNotIn(":[lhs] !is :[rhs] ==> :[lhs] is :[rhs]", text)
        self.assertNotIn(":[a~\\w+] | :[b~\\w+] ==> :[a] ^ :[b]", text)
        self.assertNotIn("uint:[n~(?:[1-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-6])] ==> int:[n]", text)
        self.assertNotIn("calculateForwardFee(:[args]) ==> calculateForwardFeeWithoutLumpPrice(:[args])", text)
        self.assertNotIn("stringSha256(:[s]) ==> stringSha256_32(:[s])", text)
        self.assertNotIn("value: ton(:[amount]) ==> value: 0", text)
        self.assertIn("BounceMode.RichBounce ==> BounceMode.NoBounce", text)
        self.assertNotIn(
            "StringBuilder.create().append(:[a]).append(:[b]).build() ==> StringBuilder.create().append(:[b]).append(:[a]).build()",
            text,
        )
