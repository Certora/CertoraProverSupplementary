methods {
    numOfKeys() returns uint envfree
    get(address) returns address envfree
}

definition IS_ADDRESS(address x) returns bool = 0 <= x && x <= max_address;

// ghost to expose the internal ordering
ghost list(uint) returns address;
ghost listLen() returns uint {
    // it's ok to assume the list length won't reach max_uint - but we may want to check that it's not possible to directly override length
    init_state axiom 0 <= listLen() && listLen() < max_uint;
    axiom listLen() < max_uint;
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

    preserved insert(address k, address _) with (env e) {
        requireInvariant mapIffInList(k);
        requireInvariant lengthLemma();
    }
}

rule boundedLengthUpdate(method f) {
    requireInvariant lengthLemma();
    uint origLen = numOfKeys();
    env e; calldataarg arg;
    f(e, arg);
    uint newLen = numOfKeys();
    assert newLen - origLen <= 1 && origLen - newLen <= 1;
}

rule checkInsert(address key, address value) {
    // a requireInvariant should be needed
    env e;
    insert(e, key, value);
    assert get(key) == value;
}

rule insertRevertConditions(address key, address value) {
    env e;
    insert@withrevert(e, key, value);
    bool succeeded = !lastReverted;

    assert (e.msg.value == 0 
        && value != 0)
        => succeeded;
}

rule inverses(address key, address value) {
    env e;
    insert(e, key, value);
    env e2;
    remove(e2, key);
    assert get(key) != value;
}

rule noChangeOther(address other, method f) {
    address pre = get(other);

    env e;
    if (f.selector == insert(address,address).selector) {
        address key;
        address value;
        require key != other;
        insert(e, key, value);
    } else if (f.selector == remove(address).selector) {
        address key;
        require key != other;
        remove(e, key);
    } else {
        calldataarg arg;
        f(e, arg);
    }
    address post = get(other);
    assert pre == post;
}

