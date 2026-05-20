// Simple Solidity example for UniversalMutator.
// The contract is intentionally small so the generated mutants are easy to inspect.

pragma solidity ^0.8.20;

/*

wer

 */

contract SimpleCounter {
    // Stored counter value.
    uint256 public value;

    constructor() {
        value = 0;
    }

    // 1 Increment the counter only while it stays below the chosen limit.
    function incrementIfBelow(uint256 limit) public returns (bool) {
        if (value < limit) {
            value = value + 1;
            return true;
        }
        return false;
    }

    // Reset the counter when it grows past the provided threshold.
    function resetIfAbove(uint256 maxValue) public {
        if (value > maxValue) {
            value = 0;
        }
    }

    // Small predicate that is easy to mutate and easy to test.
    function isZero() public view returns (bool) {
        return value == 0;
    }
}
