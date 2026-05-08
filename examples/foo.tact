// Compile-aware Tact fixture for TON mutation rules.
import "@stdlib/deploy";

message(0x12345678) Deposit {
    amount: Int as uint32;
    queryId: Int as uint64;
}

message(0x87654321) ExternalPing {
    amount: Int as uint64;
}

message(0xCAFEBABE) SerializerProbe {
    compact: Int as uint16;
    tiny: Int as uint8;
    wide: Int as uint128;
    signedWide: Int as int128;
    signed64: Int as int64;
    signed32: Int as int32;
    signed16: Int as int16;
    signed8: Int as int8;
    tail: Slice as remaining;
}

inline fun addOne(value: Int): Int {
    return value + 1;
}

fun continue(): Int {
    return 0;
}

fun break(): Int {
    return 0;
}

extends fun inspect(self: Int): Int {
    return self + 1;
}

extends mutates fun sprinkle(self: Builder, value: Int) {
    self.storeUint(value, 8);
}

contract MutationHarness {
    owner: Address;
    admin: Address;
    ownerBackup: Address?;
    maybeCell: Cell?;
    maybeSlice: Slice?;
    maybeValue: Int?;
    maybeFlag: Bool?;
    maybeText: String?;
    tinyUnsigned: Int as uint8;
    smallUnsigned: Int as uint16;
    midUnsigned: Int as uint128;
    bigUnsigned: Int as uint256;
    smallSigned: Int as int8;
    signed16Value: Int as int16;
    signed32Value: Int as int32;
    signed64Value: Int as int64;
    midSigned: Int as int128;
    bigSigned: Int as int256;
    coinsValue: Int as coins;
    counter: Int as uint32;
    store: map<Int, Int>;

    init(owner: Address) {
        self.owner = owner;
        self.admin = owner;
        self.ownerBackup = owner;
        self.maybeCell = emptyCell();
        self.maybeSlice = emptyCell().asSlice();
        self.maybeValue = 1;
        self.maybeFlag = true;
        self.maybeText = "ready";
        self.tinyUnsigned = 1;
        self.smallUnsigned = 2;
        self.midUnsigned = 3;
        self.bigUnsigned = 1;
        self.smallSigned = -1;
        self.signed16Value = -2;
        self.signed32Value = -3;
        self.signed64Value = -4;
        self.midSigned = -5;
        self.bigSigned = -1;
        self.coinsValue = 1;
        self.counter = 0;
        self.store = emptyMap();
    }

    receive(msg: Deposit) {
        require(sender() == self.owner, "owner only");

        let owner = self.owner;
        let target = self.owner;
        let minValue = 1;
        let forced = self.maybeValue!!;
        let forcedFlag = self.maybeFlag!!;
        let eq = msg.amount == forced;
        let neq = msg.amount != forced;
        let le = msg.amount <= forced;
        let ge = msg.amount >= forced;
        let ltCmp = msg.amount < forced;
        let gtCmp = msg.amount > forced;
        let missingCell = self.maybeCell == null;
        let presentText = self.maybeText != null;
        let missingSlice = self.maybeSlice == null;
        let presentFlag = self.maybeFlag != null;
        let raw = inMsg();
        let rawFromContext = context().raw;
        let ctx = context();
        let incoming = context().value;
        let fee = context().readForwardFee();
        let senderOk = sender() == owner;
        let senderBad = sender() != owner;
        let fieldOk = sender() == self.owner;
        let fieldBad = sender() != self.owner;
        let adminOk = self.admin == sender();
        let adminBad = self.admin != sender();
        let addrOk = myAddress() == target;
        let addrBad = myAddress() != target;
        let balance = myBalance();
        let debt = myStorageDue();
        let spent = gasConsumed();
        let nowTs = now();
        let lt = curLt();
        let blk = blockLt();
        let seed = getSeed();
        let rnd = randomInt();
        let nativeRnd = nativeRandom();
        let interval = nativeRandomInterval(10);
        let range = random(0, 10);
        let flipped = random(10, 0);
        let mag = abs(forced - msg.amount);
        let signum = sign(msg.amount - forced);
        let baseRound = mulShiftRight(msg.amount + 1, 5, 1);
        let rounded = mulShiftRightRound(msg.amount + 1, 5, 1);
        let ceiled = mulShiftRightCeil(msg.amount + 1, 5, 1);
        let lg = log(1024, 2);
        let lg10 = log(1024, 10);
        let pw = pow(2, 5);
        let pw10 = pow(10, 3);
        let both = eq && true;
        let either = neq || false;
        let chosen = msg.amount > forced ? msg.amount : forced;
        let minBound = min(msg.amount, forced);
        let maxBound = max(msg.amount, forced);
        let ctxSender = context().sender;
        let ctxSenderOk = ctxSender == sender();
        let builtCell = beginCell().endCell();

        let acc = msg.amount;
        acc += 5;
        acc -= 2;
        acc *= 3;
        acc /= 2;
        acc &= 7;
        acc |= 4;
        acc ^= 1;
        acc <<= 1;
        acc >>= 1;

        let sum = msg.amount + forced;
        let diff = msg.amount - forced;
        let prod = msg.amount * 2;
        let ratio = (msg.amount + 1) / 2;
        let lowBit = msg.amount & 1;
        let highBit = msg.amount | 2;
        let mixedBit = msg.amount ^ 3;
        let leftShift = msg.amount << 1;
        let rightShift = msg.amount >> 1;

        let loop = 0;
        while (loop < 1) {
            loop += 1;
        }
        let tightLoop = 0;
        while(tightLoop < 1) {
            tightLoop += 1;
        }

        let repeatCount = 1;
        repeat (repeatCount) {
            self.counter += 1;
        }
        let quickRepeat = 1;
        repeat(quickRepeat) {
            self.counter += 1;
        }

        do {
            self.counter += 1;
        } until (self.counter > 1);
        do {
            self.counter += 1;
        } until(self.counter > 2);

        let namedDefault = SendDefaultMode;
        let namedRemain = SendRemainingValue;
        let namedBalance = SendRemainingBalance;
        let namedFee = SendOnlyEstimateFee;
        let flags = SendPayGasSeparately | SendIgnoreErrors | SendRemainingValue | SendRemainingBalance;
        let moreFlags = SendPayFwdFeesSeparately | SendBounceIfActionFail | SendDestroyIfZero;
        let reserveExact = ReserveExact | ReserveBounceIfActionFail;
        let reserveMode = ReserveAllExcept | ReserveBounceIfActionFail;
        let reserveAtMost = ReserveAtMost | ReserveBounceIfActionFail;
        let reserveFlags = ReserveAddOriginalBalance | ReserveInvertSign | ReserveBounceIfActionFail;
        let localBuilder = beginCell();
        let ignoredContinue = continue();
        let ignoredBreak = break();

        let outgoingZero = SendParameters { bounce: false, mode: 0, value: 1, to: sender(), body: null };
        let outgoingTwo = SendParameters { bounce: true, mode: 2, value: 1, to: sender(), body: null };
        let outgoing = SendParameters { bounce: true, mode: 64, value: 0, to: sender(), body: null };
        let outgoingFlag1 = SendParameters { bounce: true, mode: 1, value: 0, to: sender(), body: null };
        let outgoingFlag16 = SendParameters { bounce: true, mode: 16, value: 0, to: sender(), body: null };
        let outgoingFlag32 = SendParameters { bounce: true, mode: 32, value: 0, to: sender(), body: null };
        let outgoingFlag128 = SendParameters { bounce: false, mode: 128, value: 1, to: sender(), body: null };
        let outgoingFeeOnly = SendParameters { bounce: false, mode: 1024, value: 1, to: sender(), body: null };
        let preparedBody = SendParameters { bounce: false, mode: 0, value: 1, to: sender(), body: emptyCell() };

        self.store.set(msg.amount, msg.amount + 1);
        self.store.replace(msg.amount, msg.amount + 2);
        localBuilder.sprinkle(msg.amount);

        nativeReserve(msg.amount, 0);
        nativeReserve(msg.amount, 1);
        nativeReserve(msg.amount, 2);
        nativeReserve(msg.amount, 4);
        nativeReserve(msg.amount, 8);
        nativeReserve(msg.amount, 16);
        nativeRandomize(seed);
        nativeRandomizeLt();
        nativePrepareRandom();
        setSeed(seed);

        if (context().value > fee) {
            self.counter += 1;
        }
        if (ctx.value > minValue) {
            self.counter += 1;
        }
        if (now() < nowTs + 1) {
            self.counter += 1;
        }

        if (msg.amount < -1000) {
            throw(1028);
        }
        if (msg.amount < -2000) {
            nativeThrow(1029);
        }
        throwIf(1024, msg.amount == 0);
        throwUnless(1025, msg.amount != 0);
        nativeThrowIf(1026, msg.amount == 1);
        nativeThrowUnless(1027, msg.amount != 1);
        acceptMessage();

        self.counter = addOne(self.counter) + acc.inspect();
        self.counter += sum + diff + prod + ratio + lowBit + highBit + mixedBit + leftShift + rightShift;
        self.counter += balance + debt + spent + incoming + fee + raw.bits() + rawFromContext.bits();
        self.counter += lt + blk + seed + rnd + nativeRnd + interval + range + flipped;
        self.counter += mag + signum + baseRound + rounded + ceiled + lg + lg10 + pw + pw10 + minBound + maxBound;
        self.counter += self.tinyUnsigned + self.smallUnsigned + self.midUnsigned + self.bigUnsigned;
        self.counter += self.smallSigned + self.signed16Value + self.signed32Value + self.signed64Value + self.midSigned + self.bigSigned;
        self.counter += self.coinsValue + chosen + ignoredContinue + ignoredBreak + tightLoop + quickRepeat;
        self.counter += namedDefault + namedRemain + namedBalance + namedFee + flags + moreFlags + reserveExact + reserveMode + reserveAtMost + reserveFlags;
        self.counter += outgoingZero.mode + outgoingTwo.mode + outgoing.mode + outgoingFlag1.mode + outgoingFlag16.mode + outgoingFlag32.mode + outgoingFlag128.mode + outgoingFeeOnly.mode + preparedBody.mode + builtCell.asSlice().bits();
        if (both) {
            self.counter += 1;
        }
        if (either) {
            self.counter += 1;
        }
        if (forcedFlag) {
            self.counter += 1;
        }
        if (eq || neq || le || ge || ltCmp || gtCmp || missingCell || presentText || missingSlice || presentFlag || senderOk || senderBad || fieldOk || fieldBad || adminOk || adminBad || addrOk || addrBad || ctxSenderOk) {
            self.counter += 1;
        }
    }

    external(msg: ExternalPing) {
        let outgoing = SendParameters { bounce: false, mode: 128, value: 1, to: sender(), body: null };
        let moreFlags = SendPayFwdFeesSeparately | SendBounceIfActionFail | SendDestroyIfZero;
        self.counter += msg.amount + outgoing.mode + moreFlags;
    }

    bounced(msg: bounced<Deposit>) {
        self.counter += msg.amount;
    }

    receive() {
        self.counter += 1;
    }

    receive(raw: Slice) {
        let parsed = Deposit.fromSlice(raw);
        self.counter += parsed.amount;
    }

    get fun info(): Int {
        return self.counter;
    }
}
