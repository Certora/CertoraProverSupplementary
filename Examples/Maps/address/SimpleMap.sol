pragma solidity ^0.7.0;

contract SimpleMap {
	mapping(address => address) internal map;
	function get(address key) public view returns(address) { return map[key]; }
	
	function insert(address key, address value) external {
		require(value != address(0), "0 is not a valid value");
		require (!exists(key), "key already exists");
		map[key] = value;
	}

	function remove(address key) external {
		require (map[key] != address(0), "Key does not exist");
		map[key] = address(0);
	}

	function exists(address key) internal view returns (bool) {
		if (map[key] == address(0)) {
			return false;
		}
		
		return true;
	}
}
