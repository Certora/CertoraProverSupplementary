methods {
    getToken(uint256) returns address envfree
    getIdOfToken(address) returns uint256 envfree
}
//here we defined two invarinats, one to check for corralation and one for uniqueness. 
//we require in the uniqueness invariant that the corralation is satifsfied first.
invariant existsAndUnique(uint256 index)
    (getToken(index) != 0 => getIdOfToken(getToken(index)) == index)

invariant noDuplicates(uint256 index1, uint256 index2)
    index1 != index2 => (getToken(index1) != getToken(index2) || getToken(index1) == 0)
    {
        preserved {
            requireInvariant correlateMappings(index1);
            requireInvariant correlateMappings(index2);
        }
    }


rule integerityOfCount(method f) filtered{f->!f.isView}{
    env e;
    calldataarg args;
    uint reserveCountBefore = getReserveCount(e);
    f(e, args);
    uint reserveCountAfter = getReserveCount(e);
    assert reserveCountBefore - reserveCountAfter == 1 || reserveCountAfter - reserveCountBefore == 1;
}