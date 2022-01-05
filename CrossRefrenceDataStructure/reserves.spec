methods {
    getTokenAtIndex(uint256) returns address envfree
    getIdOfToken(address) returns uint256 envfree
}
//here we define two macros for readabilty, one macro is for the corralation condition and one for the uniqueness condition
definition corralates(uint256 index) returns bool = getTokenAtIndex(index) != 0 => getIdOfToken(getTokenAtIndex(index)) == index;
definition checkDuplicates(uint256 index1, uint256 index2) returns bool = index1 != index2 => (getTokenAtIndex(index1) != getTokenAtIndex(index2) || getTokenAtIndex(index1) == 0);
invariant existsAndUnique(uint256 index1, uint256 index2)
    corralates(index1) && corralates(index2) && checkDuplicates(index1, index2)


rule integerityOfCount(method f) filtered{f->!f.isView}{
    env e;
    calldataarg args;
    uint reserveCountBefore = getReserveCount(e);
    f(e, args);
    uint reserveCountAfter = getReserveCount(e);
    assert reserveCountBefore - reserveCountAfter == 1 || reserveCountAfter - reserveCountBefore == 1;
}

