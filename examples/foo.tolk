const ERR = 41
const ERR_INVALID_OP = 63

struct (0x12345678) CounterIncrement {
    incBy: uint32
    decBy: int32
}

struct (0x01) ShortPrefix {
    value: uint8
}

struct AuctionConfig {
    ownerAddress: address? = null
    minBid: coins = 0
    priceStep: uint16 = 1
}

type AllowedMessage = CounterIncrement | ShortPrefix

struct FeeWindow {
    due: coins
    paid: coins
}

struct WalletShim {
}

fun FeeWindow.getStorageDuePayment(self): coins {
    return self.due;
}

fun FeeWindow.getStoragePaidPayment(self): coins {
    return self.paid;
}

fun WalletShim.save(mutate self) {
}

fun calculateForwardFee(cells: int, bits: int, isMasterchain: bool): coins {
    return cells + bits;
}

fun calculateForwardFeeWithoutLumpPrice(cells: int, bits: int, isMasterchain: bool): coins {
    return cells + bits;
}

fun calculateGasFee(isMasterchain: int, gasUsed: int): coins {
    return isMasterchain + gasUsed;
}

fun calculateGasFeeWithoutFlatPrice(isMasterchain: int, gasUsed: int): coins {
    return isMasterchain + gasUsed;
}

fun acceptExternalMessage() {}

fun dict.iDictGetFirst(self, keyBits: int) {
    return keyBits;
}

fun dict.uDictGetLast(self, keyBits: int) {
    return keyBits;
}

fun dict.uDictDeleteFirstAndGet(self, keyBits: int) {
    return keyBits;
}

fun dict.uDictDeleteLastAndGet(self, keyBits: int) {
    return keyBits;
}

fun dict.iDictGetNextOrEqual(self, keyBits: int, pivot: int) {
    return keyBits + pivot;
}

fun dict.iDictGetPrevOrEqual(self, keyBits: int, pivot: int) {
    return keyBits + pivot;
}

fun dict.iDictGetNext(self, keyBits: int, pivot: int) {
    return keyBits + pivot;
}

fun dict.uDictGetPrev(self, keyBits: int, pivot: int) {
    return keyBits + pivot;
}

fun dict.uDictGetNext(self, keyBits: int, pivot: int) {
    return keyBits + pivot;
}

fun dict.uDictGetNextOrEqual(self, keyBits: int, pivot: int) {
    return keyBits + pivot;
}

fun dict.uDictGetPrevOrEqual(self, keyBits: int, pivot: int) {
    return keyBits + pivot;
}

fun address.isInternal(self): bool {
    return true;
}

fun address.isExternal(self): bool {
    return false;
}

@inline
fun inlineFn(a: int, delta: int = 1): int {
    return a + delta;
}

fun leadingDefaults(a: int = 1, b: int = 2): int {
    return a + b;
}

fun middleDefaults(a: int, b: int = 1, c: int = 2): int {
    return a + b + c;
}

@noinline
fun noinlineFn(a: int): int {
    return a;
}

@inline_ref
fun refFn(a: int): int {
    return a;
}

@pure
@method_id(123)
fun taggedFn(): int {
    return 1;
}

fun CounterIncrement.bump(mutate self): self {
    self.incBy += 1;
    self.decBy -= 1;
    return self;
}

fun helper(mutate cs: slice, mutate amount: int, target: Cell<address>?, body: slice) {
    assert (amount > 0) throw ERR;
    var parsed = target!;
    var msg = AllowedMessage.fromSlice(body, { throwIfOpcodeDoesNotMatch: ERR_INVALID_OP });
    amount += cs.remainingBitsCount();
    return (cs, amount, parsed, msg);
}

fun sideEffectCoverage(flag: bool, code: cell, mutate wallet: WalletShim) {
    if(flag) {
        throw ERR;
    }
    wallet.save();
    contract.setData(code);
    contract.setCodePostponed(code);
}

fun optionCoverage(body: slice) {
    var strictTail = AllowedMessage.fromSlice(body, { assertEndAfterReading: true });
    var looseTail = AllowedMessage.fromSlice(body, { assertEndAfterReading: false });
    return (strictTail, looseTail);
}

fun returnUnaryCoverage(flag: bool, amount: int): int {
    var denied = !flag;
    var inverted = ~amount;
    var negated = -amount;
    var acc = amount;

    acc %= 3;
    if(flag) {
        return ~amount;
    }
    if (denied) {
        return -amount;
    }
    return inverted + negated;
}

fun boolUnaryCoverage(flag: bool): bool {
    return !flag;
}

fun compareCoverage(a: int, b: int): int {
    assert (a == b) throw ERR;
    assert (a != b) throw ERR;
    assert (a >= b) throw ERR;
    assert (a <= b) throw ERR;
    if (a == b) {
        return 1;
    }
    if (a != b) {
        return 2;
    }
    if (a >= b) {
        return 3;
    }
    if (a <= b) {
        return 4;
    }
    return 0;
}

fun compareAndBitsCoverage(a: int, b: int): bool {
    assert (a < b) throw ERR;
    assert (a > b) throw ERR;
    var bits = a | b;

    if (a < b) {
        return a > b;
    }
    if (a > b) {
        return a < b;
    }
    return bits > 0;
}

get fun currentCounter(): int {
    return 0;
}

fun coverageOps(flag: bool): int {
    var a = 10;
    var b = 6;
    var steps = 0;
    var count = 1;

    a += 5;
    b -= 6;
    a *= 2;
    b /= 2;
    a &= 7;
    b |= 3;
    a ^= 1;
    a <<= 1;
    b >>= 1;

    var shiftedLeft = a << 1;
    var shiftedRight = b >> 1;
    var masked = a & b;
    var mixed = a | b;
    var flipped = a ^ b;
    var truthy = true;
    var falsy = false;

    while (steps < 2) {
        steps += 1;
    }
    while (steps < 3) {
        steps += 1;
    }
    repeat (count) {
        a += 1;
    }
    repeat (count) {
        b += 1;
    }

    // break
    // continue
    if (flag && truthy && !falsy) {
        return a + b;
    }
    return a + b + shiftedLeft + shiftedRight + masked + mixed + flipped;
}

fun castNumber(flag: bool, a: uint64, b: int64): int {
    var x = a as uint32;
    var y = b as int32;
    var z: varuint16 = 0;
    var zWide: varuint32 = 0;
    var zSigned: varint16 = 0;
    var zSignedWide: varint32 = 0;
    var tinyUnsigned = a as uint8;
    var smallUnsigned = a as uint16;
    var signedFromUnsigned = a as int64;
    var signedTiny = a as int8;
    var unsignedFromSigned = b as uint32;
    var unsignedWide = b as uint64;
    var signedNarrow = b as int16;
    if (flag && true) {
        z += 1;
    }
    return x + y + z + zWide + zSigned + zSignedWide + tinyUnsigned + smallUnsigned +
    signedFromUnsigned +
    signedTiny +
    unsignedFromSigned +
    unsignedWide +
    signedNarrow;
}

fun stdlibOps(c: cell, other: cell, dest: address) {
    var nowTs = blockchain.now();
    var lt = blockchain.logicalTime();
    var blockLt = blockchain.currentBlockLogicalTime();
    var csz = c.calculateSizeStrict(10);
    var ssz = c.beginParse().calculateSize(10);
    var fwd = calculateForwardFee(0, 100, true);
    var fwdNoLump = calculateForwardFeeWithoutLumpPrice(0, 100, true);
    var gas = calculateGasFee(0, 100);
    var gasNoFlat = calculateGasFeeWithoutFlatPrice(0, 100);
    var rnd = random.uint256();
    var seed = random.getSeed();
    acceptExternalMessage();
    commitContractDataAndActions();

    var feeWindow = FeeWindow { due: 1, paid: 2 };
    var dueFee = feeWindow.getStorageDuePayment();
    var paidFee = feeWindow.getStoragePaidPayment();

    var messageBuilder = beginCell().storeMessageOp(0x44).storeMessageQueryId(7);
    var messageSlice = messageBuilder.endCell().beginParse();
    var manualOp = messageSlice.loadMessageOp();
    var manualQuery = messageSlice.loadMessageQueryId();

    var builder = beginCell().storeInt(-1, 8).storeUint(2, 8).storeRef(other).storeMaybeRef(other)
        .storeDict(null);
    var body = builder.endCell().beginParse();
    var nextRef = body.preloadRef();
    var loadedRef = body.loadRef();
    var nextMaybeRef = body.preloadMaybeRef();
    var loadedMaybeRef = body.loadMaybeRef();
    var loadedInt = body.loadInt(8);
    var preloadedInt = body.preloadInt(8);
    var loadedUint = body.loadUint(8);
    var preloadedUint = body.preloadUint(8);
    var loadedBits = body.loadBits(8);
    var preloadedBits = body.preloadBits(8);
    var loadedDict = body.loadDict();
    var preloadedDict = body.preloadDict();
    var remainingBits = body.remainingBitsCount();
    var remainingRefs = body.remainingRefsCount();
    var empty = body.isEmpty();
    var endBits = body.isEndOfBits();
    var endRefs = body.isEndOfRefs();
    var firstBits = messageSlice.getFirstBits(16);
    var lastBits = messageSlice.getLastBits(16);
    var internalKind = dest.isInternal();
    var externalKind = dest.isExternal();
    var firstSigned = loadedDict.iDictGetFirst(256);
    var lastUnsigned = loadedDict.uDictGetLast(256);
    var deletedSigned = loadedDict.uDictDeleteFirstAndGet(256);
    var deletedUnsigned = loadedDict.uDictDeleteLastAndGet(256);
    var nextSigned = loadedDict.iDictGetNextOrEqual(256, 1);
    var prevSigned = loadedDict.iDictGetPrevOrEqual(256, 1);
    var nextOnlySigned = loadedDict.iDictGetNext(256, 1);
    var prevUnsigned = loadedDict.uDictGetPrev(256, 1);
    var nextUnsigned = loadedDict.uDictGetNext(256, 1);
    var nextOrEqualUnsigned = loadedDict.uDictGetNextOrEqual(256, 1);
    var prevOrEqualUnsigned = loadedDict.uDictGetPrevOrEqual(256, 1);

    return (
        nowTs,
        lt,
        blockLt,
        csz,
        ssz,
        fwd,
        fwdNoLump,
        gas,
        gasNoFlat,
        rnd,
        seed,
        dueFee,
        paidFee,
        manualOp,
        manualQuery,
        nextRef,
        loadedRef,
        nextMaybeRef,
        loadedMaybeRef,
        loadedInt,
        preloadedInt,
        loadedUint,
        preloadedUint,
        loadedBits,
        preloadedBits,
        loadedDict,
        preloadedDict,
        remainingBits,
        remainingRefs,
        empty,
        endBits,
        endRefs,
        firstBits,
        lastBits,
        internalKind,
        externalKind,
        firstSigned,
        lastUnsigned,
        deletedSigned,
        deletedUnsigned,
        nextSigned,
        prevSigned,
        nextOnlySigned,
        prevUnsigned,
        nextUnsigned,
        nextOrEqualUnsigned,
        prevOrEqualUnsigned
    );
}

fun computedValue(): coins {
    return ton("0.03");
}

fun sendModes(dest: address, msgCell: cell) {
    val regular = createMessage({
        bounce: BounceMode.NoBounce,
        dest,
        value: 0,
        body: CounterIncrement { incBy: 1, decBy: -1 },
    });
    val rich = createMessage({
        bounce: BounceMode.RichBounceOnlyRootCell,
        dest,
        value: 1,
        body: ShortPrefix { value: 7 },
    });
    val shortBody = createMessage({
        bounce: BounceMode.Only256BitsOfBody,
        dest,
        value: ton("0.01"),
        body: CounterIncrement { incBy: 2, decBy: -2 },
    });
    val dynamicValue = createMessage({
        bounce: BounceMode.NoBounce,
        dest,
        value: computedValue(),
        body: ShortPrefix { value: 9 },
    });

    regular.send(SEND_MODE_REGULAR);
    regular.send(1);
    regular.send(2);
    regular.send(16);
    regular.send(32);
    regular.send(64);
    regular.send(128);
    regular.send(1024);
    regular.sendAndEstimateFee(0);
    regular.sendAndEstimateFee(1);
    regular.sendAndEstimateFee(2);
    regular.sendAndEstimateFee(16);
    regular.sendAndEstimateFee(32);
    regular.sendAndEstimateFee(64);
    regular.sendAndEstimateFee(128);
    regular.sendAndEstimateFee(1024);
    rich.estimateFeeWithoutSending(0);
    rich.estimateFeeWithoutSending(1);
    rich.estimateFeeWithoutSending(2);
    rich.estimateFeeWithoutSending(16);
    rich.estimateFeeWithoutSending(32);
    rich.estimateFeeWithoutSending(64);
    rich.estimateFeeWithoutSending(128);
    rich.estimateFeeWithoutSending(1024);
    rich.estimateFeeWithoutSending(SEND_MODE_IGNORE_ERRORS |
    SEND_MODE_CARRY_ALL_REMAINING_MESSAGE_VALUE);
    shortBody.send(SEND_MODE_PAY_FEES_SEPARATELY | SEND_MODE_BOUNCE_ON_ACTION_FAIL);
    dynamicValue.send(SEND_MODE_ESTIMATE_FEE_ONLY);
    dynamicValue.send(SEND_MODE_DESTROY);
    sendRawMessage(msgCell, 0);
    sendRawMessage(msgCell, 1);
    sendRawMessage(msgCell, 2);
    sendRawMessage(msgCell, 16);
    sendRawMessage(msgCell, 32);
    sendRawMessage(msgCell, 64);
    sendRawMessage(msgCell, 128);
    sendRawMessage(msgCell, 1024);
    sendRawMessage(msgCell, SEND_MODE_IGNORE_ERRORS | SEND_MODE_CARRY_ALL_REMAINING_MESSAGE_VALUE);
    sendRawMessage(msgCell, SEND_MODE_PAY_FEES_SEPARATELY | SEND_MODE_BOUNCE_ON_ACTION_FAIL);
    sendRawMessage(msgCell, SEND_MODE_CARRY_ALL_BALANCE);
    reserveToncoinsOnBalance(ton("0.01"), 0);
    reserveToncoinsOnBalance(ton("0.01"), 1);
    reserveToncoinsOnBalance(ton("0.01"), 2);
    reserveToncoinsOnBalance(ton("0.01"), RESERVE_MODE_AT_MOST);
    reserveToncoinsOnBalance(ton("0.01"), RESERVE_MODE_EXACT_AMOUNT);
    reserveToncoinsOnBalance(ton("0.01"), RESERVE_MODE_ALL_BUT_AMOUNT);
    reserveToncoinsOnBalance(ton("0.01"), RESERVE_MODE_INCREASE_BY_ORIGINAL_BALANCE);
    reserveToncoinsOnBalance(ton("0.01"), RESERVE_MODE_NEGATE_AMOUNT);
    reserveToncoinsOnBalance(ton("0.01"), RESERVE_MODE_BOUNCE_ON_ACTION_FAIL);
    reserveExtraCurrenciesOnBalance(ton("0.01"), null, 0);
    reserveExtraCurrenciesOnBalance(ton("0.01"), null, 1);
    reserveExtraCurrenciesOnBalance(ton("0.01"), null, 2);
}

fun stringsOps(metadataUri: string) {
    val oldCrc = stringCrc32("legacy");
    val oldSmall = stringCrc16("legacy");
    val oldHash = stringSha256("legacy");
    val oldMinihash = stringSha256_32("legacy");
    return (metadataUri, oldCrc, oldSmall, oldHash, oldMinihash);
}

fun classify(value: AllowedMessage | null, body: slice): int {
    val lazyMsg = lazy AllowedMessage.fromSlice(body);
    val msg = AllowedMessage.fromSlice(body);
    var preview: int = match (lazyMsg) {
        CounterIncrement => lazyMsg.incBy,
        ShortPrefix => lazyMsg.value,
    };
    if (value is CounterIncrement && true) {
        var noBounce = BounceMode.NoBounce;
        var rich = BounceMode.RichBounce;
        var root = BounceMode.RichBounceOnlyRootCell;
        var shortBody = BounceMode.Only256BitsOfBody;
        value.bump();
        return value.incBy + preview;
    }
    if (msg !is CounterIncrement) {
        return 0;
    }
    return msg.incBy;
}

fun onBouncedMessage(in: InMessageBounced) {
    // no-op on purpose
}

fun onInternalMessage(in: InMessage) {
    // no-op on purpose
}
