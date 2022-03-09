pragma solidity < 0.8;

library SafeMath {
	function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

	function safeSub(uint256 x, uint256 y) internal pure returns(uint256) {
		assert(x >= y);
		return x - y;
    }
}

contract Counter {
	using SafeMath for uint256;
	
	address public admin;
	uint public counter;
		
	function inc() public returns (uint) {
		require(msg.sender == admin);
		return counter = counter.safeAdd(1);
	}
	
	function dec() public returns (uint) {
		require(msg.sender == admin);
		return counter = counter.safeSub(1);
	}
}

