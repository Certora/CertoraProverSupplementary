/*
 * This is a specification file to formally verify BorrowSystem.sol
 * smart contract using the Certora Prover. For more information,
 * visit: https://www.certora.com/
 *
 * To run, use: Examples/Liquidate/run.sh
 */

using DummyERC20A as collateralToken
using DummyERC20B as borrowToken

/*
 * Declaration of methods that are used in the rules.
 * envfree indicates that the method is not dependent 
 * on the environment (msg.value, msg.sender). Methods
 * that are not declared here are assumed to be dependent
 * on environment.
 */
methods {
	// ERC20 functions
	collateralToken.balanceOf(address user) returns (uint256) envfree;
	borrowToken.balanceOf(address user) returns (uint256) envfree;

	// State mapping variables
	userBorrowAmount(address user) returns (uint256) envfree;
	userCollateralAmount(address user) returns (uint256) envfree;

	// NONDET is a function summary that allows developers to express the
	// return value of a function as a nondeterministic value. Since
	// get, a function of the IOracle, is external, we summarize its return
	// value as NONDET (nondeterministic).
	get(address token1, address token2) returns (uint256) => NONDET;
}

/*
 * Invariants:
 * They are a property of the program state that is always true. For example,
 * elements are always popped from the top of a stack. The condition has to
 * hold for the constructor as well.
 */

/*
 * If a user has borrowed amount, they must have deposited some collateral.
 */
invariant onlyCollateralCanBorrow(address user)
	userBorrowAmount(user) > 0 => userCollateralAmount(user) > 0

/*
 * Rules:
 * Given some pre-conditions, what are the desired post conditions after some
 * operation is executed. Can be mathematical properties, about the state,
 * or more. For example, assets should be preserved etc.
 */

/*
 * When someone is liquidated, the following should be true about the system:
 *     If borrow increased, then collateral must decrease
 *     If collateral decreased, then borrow must increase
 */
rule antimonotonicityOfLiquidation () {
	env e;
	address user;
	address to;

	uint256 collateralBefore = collateralToken.balanceOf(currentContract);
	uint256 borrowBefore = borrowToken.balanceOf(currentContract);

	requireInvariant onlyCollateralCanBorrow(user);
	require( to != currentContract );

	liquidate(e, user, to);

	uint256 collateralAfter = collateralToken.balanceOf(currentContract);
	uint256 borrowAfter = borrowToken.balanceOf(currentContract);

	// <=> ---> A double implication
	assert(borrowBefore < borrowAfter <=> collateralBefore > collateralAfter);
}

