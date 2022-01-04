methods {
    getToken(uint256) returns address envfree
    getIdOfToken(address) returns uint256 envfree
}

invariant correlateMappings(uint256 index1, uint256 index2)
    (getToken(index1) != 0 => getIdOfToken(getToken(index1)) == index1) && (getToken(index2) != 0 => getIdOfToken(getToken(index2)) == index2) && (index1 != index2 => (getToken(index1) != getToken(index2) || getToken(index1) == 0))

// invariant noDuplicates(uint256 index1, uint256 index2)
//     index1 != index2 => (getToken(index1) != getToken(index2) || getToken(index1) == 0)
//     {
//         preserved {
//             requireInvariant correlateMappings(index1);
//             requireInvariant correlateMappings(index2);
//         }
//     }


rule integerityOfCount(method f) filtered{f->!f.isView}{
    env e;
    calldataarg args;
    uint reserveCountBefore = getReserveCount(e);
    f(e, args);
    uint reserveCountAfter = getReserveCount(e);
    assert reserveCountBefore - reserveCountAfter == 1 || reserveCountAfter - reserveCountBefore == 1;
}

