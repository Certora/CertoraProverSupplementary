methods {
    get(address) returns address envfree
    existsKey(address) returns bool envfree
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

rule checkIterate() {
    env e;
    iterate(e);
    address someKey;
    require existsKey(someKey);
    assert get(someKey) == 123;
}