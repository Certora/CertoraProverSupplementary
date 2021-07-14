

using DummyERC20A as collateralToken
using DummyERC20B as borrowToken

methods{
	collateralToken.balanceOf(address u) returns (uint256) envfree;
	borrowToken.balanceOf(address u) returns (uint256) envfree;
	userBorrowAmount(address u) returns (uint256) envfree;
	userCollateralAmount(address u) returns (uint256) envfree;
	get(address token1, address token2) returns (uint256) => NONDET;
}

invariant onlyCollateralCanBorrow(address user)
	userBorrowAmount(user) > 0 => userCollateralAmount(user) > 0



rule validChangeToBalances() {
	env e;
	address user;
	address to;

	uint256 collateralBefore = collateralToken.balanceOf(currentContract);
	uint256 borrowBefore = borrowToken.balanceOf(currentContract);
	requireInvariant onlyCollateralCanBorrow(user);

	liquidate(e, user, to);

	uint256 collateralAfter = collateralToken.balanceOf(currentContract);
	uint256 borrowAfter = borrowToken.balanceOf(currentContract);
	assert ( borrowBefore < borrowAfter <=> collateralBefore > collateralAfter );
}