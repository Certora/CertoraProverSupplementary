methods {
    numOfKeys() returns uint envfree
    get(address) returns address envfree
}

// consts and simple macro definitions
definition MAX_UINT256() returns uint256 = 2^256 - 1;
definition MAX_UINT160() returns uint256 = 2^160 - 1;

definition IS_ADDRESS(address x) returns bool = 0 <= x && x <= MAX_UINT160();

// ghost to expose the internal ordering
ghost list(uint) returns address;
ghost listLen() returns uint {
    // it's ok to assume the list length won't reach MAX_UINT256 - but we may want to check that it's not possible to directly override length
    init_state axiom 0 <= listLen() && listLen() < MAX_UINT256();
    axiom listLen() < MAX_UINT256();
}

// hooks
// establish the length
hook Sstore keys uint lenNew STORAGE {
    // the length of a solidity storage array is at the variable's slot
    havoc listLen assuming listLen@new() == lenNew;
}

// establish the ghost list (so that it can be used in quantified contexts)
hook Sload address n keys[INDEX uint index] STORAGE {
    require list(index) == n;
}

hook Sstore keys[INDEX uint index] address n STORAGE {
    require IS_ADDRESS(n);
    havoc list assuming list@new(index) == n &&
        (forall uint i. i != index => list@new(i) == list@old(i));
}

// a predicate for checking if an address is listed (in the underlying list, not in the map)
definition isListed(address a, uint i) returns bool = 0 <= i && i < listLen() && list(i) == a;

invariant lengthLemma() listLen() == numOfKeys()

// establish that the map and the list hold the same keys
invariant mapIffInList(address a) /*a != 0 =>*/ (get(a) != 0 <=> (exists uint i. isListed(a, i))) {
    preserved insert(address _, address _) with (env e) {
        requireInvariant lengthLemma();
    }

    preserved remove(address b) with (env e) {
        if (get(b) != 0) {
            requireInvariant listIsSet(b); // cannot have another instance of the removed asset
        }
        requireInvariant lengthLemma();
    }
}

// establish that the list doesn't contain duplicate elements
invariant listIsSet(address a) forall uint i. isListed(a, i) => (forall uint j. isListed(a, j) => j == i) {
    preserved {
        requireInvariant lengthLemma();
    }
}

rule boundedLengthUpdate(method f) {
    uint origLen = numOfKeys();
    env e; calldataarg arg;
    f(e, arg);
    uint newLen = numOfKeys();
    assert newLen - origLen <= 1 && origLen - newLen <= 1;
}

rule checkInsert(address key, address value) {
    env e;
    insert(e, key, value);
    assert get(key) == value;
}