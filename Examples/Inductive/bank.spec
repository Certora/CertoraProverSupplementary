 
methods {
	getTotal() returns uint256 envfree
	getBalanceBob() returns uint256 envfree
    getBalanceAlice() returns uint256 envfree
}

invariant ConsistentTotal() getTotal() == (getBalanceAlice()+getBalanceBob())

invariant smallerTotal() getBalanceAlice() <= getTotal() && getBalanceBob() <= getTotal()
