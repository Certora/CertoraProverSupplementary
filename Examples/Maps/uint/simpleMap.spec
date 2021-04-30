methods {
    get(uint) returns uint envfree
    contains(uint) returns bool envfree
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

