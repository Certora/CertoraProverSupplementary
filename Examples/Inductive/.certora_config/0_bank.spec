 
methods {
	getTotal() returns uint256 envfree
	getBalanceBob() returns uint256 envfree
        getBalanceAlice() returns uint256 envfree
}


invariant smallerTotal() getBalanceAlice() <= getTotal() && getBalanceBob() <= getTotal() // This invariant is not inductive.



rule noOverFlow1(uint256 amount) {
    require  getTotal() + amount <= max_uint; // No overflow
    requireInvariant smallerTotal();
    assert getBalanceAlice() + amount  <= max_uint, "potential overflow in Deposit of Alice" ;
    assert getBalanceBob() + amount  <= max_uint, "potential overflow in Deposit of Bob" ;          
}

invariant consistentTotal() getTotal() == (getBalanceAlice()+getBalanceBob()) // This invariant is inductive.

rule noOverFlow2(uint256 amount) {
    require  getTotal() + amount <= max_uint; // No overflow
    requireInvariant consistentTotal();
    assert getBalanceAlice() + amount  <= max_uint, "potential overflow in Deposit of Alice" ;
    assert getBalanceBob() + amount  <= max_uint, "potential overflow in Deposit of Bob" ;          
}