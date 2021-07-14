// SPDX-License-Identifier: agpl-3.0
// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.0;

interface IERC20 {
	function transfer(address to, uint value) external ;
    function transferFrom(address from, address to, uint value) external;
}

interface IOracle {
	function get(IERC20 token1, IERC20 token2) external returns (uint256);

}


contract SimpleBorrowSystem {

	// amount of borrowToken user borrowed
	mapping(address => uint256) public userBorrowAmount;

	// amount of collateralToken user has deposited
	mapping(address => uint256) public userCollateralAmount;

	// ERC20 collateralToken
	IERC20 collateralToken;

	// ERC20 borrow token 
	IERC20 borrowToken;

	/* Borrow amount and provide collateral */
	function borrow(uint256 borrowAmount, uint256 collateralAmount) public {
		userBorrowAmount[msg.sender] += borrowAmount;
		userCollateralAmount[msg.sender] += collateralAmount;
		require (_isSolvent(msg.sender), "user is not solvent");
		borrowToken.transferFrom(msg.sender, address(this), borrowAmount);
		collateralToken.transfer(msg.sender, collateralAmount);
	}

	/* Repay part of a user's borrow and get back a part of his collateral */
	function repay(uint256 borrowAmount, uint256 collateralAmount) public {
		userBorrowAmount[msg.sender] -= borrowAmount;
		userCollateralAmount[msg.sender] -= collateralAmount;
		require (_isSolvent(msg.sender), "user is not solvent");
        borrowToken.transferFrom(msg.sender, address(this), borrowAmount);
		collateralToken.transfer(msg.sender, collateralAmount);
	}

	/* Liquidation of a user that is in insolvent state.
		user - address to liquidate
		to - address to receive collateral
	*/ 
	function liquidate(
        address user,
        address to
    ) public {
        // Oracle can fail but we still need to allow liquidations
        require (!_isSolvent(user), "user is solvent");
		uint256 borrow = userBorrowAmount[user];
        uint256 collateral = userCollateralAmount[user];
		//require( borrow > 0 && collateral > 0);
    	userBorrowAmount[user] = 0;
		userCollateralAmount[user] = 0;
        borrowToken.transferFrom(msg.sender, address(this), borrow);
        collateralToken.transfer(to, collateral);
	}
	


	uint8 internal constant CALL_BORROW = 1;
	uint8 internal constant CALL_REPAY = 2;
	uint8 internal constant CALL_LIQUIDATE = 3;
	/*
		Allows calling a few functions in a batch mode and interaction with other contracts
	*/
	function batchCalls(
        uint8[] calldata actions,
        uint256[] calldata borrowAmount,
		uint256[] calldata collateralAmount,
		address[] calldata callee,
        bytes[] calldata datas
    ) external  {
        for (uint256 i = 0; i < actions.length; i++) {
            uint8 action = actions[i];
            if (action == CALL_BORROW) {
                borrow(borrowAmount[i], collateralAmount[i]);
            } else if (action == CALL_REPAY) {
                repay(borrowAmount[i], collateralAmount[i]);
			}
            else {
				require(callee[i] != address(collateralToken) && callee[i] != address(borrowToken));
				 callee[i].call(datas[i]);
			}
			
        }
	}

	/* Check if a user's collateral balance covers his borrow according to the current price.
		Returns true when the user is solvent

	*/
	IOracle oracle; 
	function _isSolvent(address user) private returns (bool)  {
		uint256 rate = oracle.get(borrowToken, collateralToken);
		require(rate !=0);
		return userBorrowAmount[user] * rate < userCollateralAmount[user];
	}

}