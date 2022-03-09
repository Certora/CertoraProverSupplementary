pragma solidity < 0.8;

contract Counter {
	address public admin;
	uint public counter;
		
	function inc() public returns (uint) {
		require(msg.sender == admin);
		return ++counter;
	}
	
	function dec() public returns (uint) {
		require(msg.sender == admin);
		return --counter;
	}
}

