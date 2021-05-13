methods {
	getTotal() returns uint256 envfree
    balances(address) returns uint256 envfree
}

ghost ghostTotal() returns uint256;

hook Sstore balances[KEY address account] uint256 amount (uint256 old_amount) STORAGE {
    havoc ghostTotal assuming ghostTotal@new() == ghostTotal@old() + amount - old_amount;
}

invariant smallerTotal() forall address a. balances(a) <= ghostTotal() // This invariant is not inductive.

rule invariantAsARule(method f, env e, calldataarg args) {
    address a;
    require forall address b. balances(b) <= ghostTotal();
    f@withrevert(e, args);
    assert balances(a) <= ghostTotal();
}