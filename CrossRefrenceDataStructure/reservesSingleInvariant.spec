methods {
    getTokenAtIndex(uint256) returns address envfree
    getIdOfToken(address) returns uint256 envfree
}
//here we check all the invariants in one invariant
invariant existsAndUnique(uint256 index1, uint256 index2)
    (getTokenAtIndex(index1) != 0 => getIdOfToken(getTokenAtIndex(index1)) == index1) && (getTokenAtIndex(index2) != 0 => getIdOfToken(getTokenAtIndex(index2)) == index2) && (index1 != index2 => (getTokenAtIndex(index1) != getTokenAtIndex(index2) || getTokenAtIndex(index1) == 0))


rule integerityOfCount(method f) filtered{f->!f.isView}{
    env e;
    calldataarg args;
    uint reserveCountBefore = getReserveCount(e);
    f(e, args);
    uint reserveCountAfter = getReserveCount(e);
    assert reserveCountBefore - reserveCountAfter == 1 || reserveCountAfter - reserveCountBefore == 1;
}

