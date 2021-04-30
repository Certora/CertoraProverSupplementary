pragma solidity ^0.7.0;

contract SimpleMap {
	mapping(uint => uint) internal map;
	function get(uint key) public view returns(uint) { return map[key]; }
	
	function insert(uint key, uint value) external {
		require(value != uint(0), "0 is not a valid value");
		require (!contains(key), "key already exists");
		map[key] = value;
	}

	function remove(uint key) external {
		require (map[key] != uint(0), "Key does not exist");
		map[key] = uint(0);
	}

	function contains(uint key) public view returns (bool) {
		if (map[key] == uint(0)) {
			return false;
		}
		
		return true;
	}
}
