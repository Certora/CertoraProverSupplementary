methods {
    get(uint) returns uint envfree
    contains(uint) returns bool envfree
}

// key to value
ghost _map(uint) returns uint;
// index to key
ghost array(uint) returns uint;
// array length
ghost arrayLen() returns uint;

// hooks for map
hook Sload uint v map[KEY uint k] STORAGE {
    require _map(k) == v;
}

hook Sstore map[KEY uint k] uint v STORAGE {
    havoc _map assuming _map@new(k) == v &&
        (forall uint k2. k2 != k => _map@new(k2) == _map@old(k2));
}

// hooks for array
hook Sload uint n keys[INDEX uint index] STORAGE {
    require array(index) == n;
}

hook Sstore keys[INDEX uint index] uint n STORAGE {
    havoc array assuming array@new(index) == n &&
        (forall uint i. i != index => array@new(i) == array@old(i));
}

// hooks for arrayLen
hook Sstore keys uint lenNew STORAGE {
    // the length of a solidity storage array is at the variable's slot
    havoc arrayLen assuming arrayLen@new() == lenNew;
}

rule checkInsert(uint key, uint value) {
    env e;
    insert(e, key, value);
    assert get(key) == value, "value of key is not equal to the inserted value";
}

rule checkContains(bool isInsert) {
    env e;
    uint someKey;
    if (isInsert) {    
        uint someValue;
        insert(e, someKey, someValue);
        assert contains(someKey), "insertion should imply containment";
    } else {
        remove(e, someKey);
        assert !contains(someKey), "removal should imply the key is not contained anymore";
    }
}

rule insertRevertConditions(uint key, uint value) {
    env e;
    insert@withrevert(e, key, value);
    bool succeeded = !lastReverted;

    assert (e.msg.value == 0 
        && value != 0
        && !contains(key))
        => succeeded;
}

rule inverses(uint key, uint value) {
    env e;
    insert(e, key, value);
    env e2;
    require e2.msg.value == 0;
    remove@withrevert(e2, key);
    bool removeSucceeded = !lastReverted;
    assert removeSucceeded, "remove after insert must succeed";
    assert get(key) != value, "value of removed key must not be the inserted value";
}

rule checkIterate() {
    env e;
    iterate(e);
    uint someKey;    
    require contains(someKey);
    assert get(someKey) == 100;
}

rule noChangeOther(uint other, method f) {
    uint pre = get(other);

    env e;
    if (f.selector == insert(uint256,uint256).selector) {
        uint key;
        uint value;
        require key != other;
        insert(e, key, value);
    } else if (f.selector == remove(uint256).selector) {
        uint key;
        require key != other;
        remove(e, key);
    } else {
        calldataarg arg;
        f(e, arg);
    }

    uint post = get(other);
    assert pre == post;
}

// ghost checks
invariant checkMapGhost(uint someKey) get(someKey) == _map(someKey)