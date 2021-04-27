pragma solidity ^0.7.0;

/**
A simple enumerable map.
Override the contract to implement custom iterators.
 */
contract SimpleEnumerableMap {
	mapping(address => address) internal map;
	address[] internal keys;

	function numOfKeys() external view returns (uint) { return keys.length; }

	function get(address key) public view returns(address) { return map[key]; }
	
	function insert(address key, address value) external {
		require(value != address(0), "0 is not a valid value");
		if (!exists(key)) {
			map[key] = value;
			keys.push(key);
		} else {
			map[key] = value;
		}
	}

	function remove(address key) external {
		require (map[key] != address(0), "Key does not exist");
		map[key] = address(0);
		uint i = indexOf(key);
		if (i < keys.length - 1) {
			keys[i] = keys[keys.length-1];
		}
		keys.pop();
	}

	function exists(address key) internal view returns (bool) {
		if (map[key] == address(0)) {
			return false;
		}
		for (uint i = 0 ; i < keys.length ; i++) {
			if (keys[i] == key) {
				return true;
			}
		}
		return false;
	}

	function indexOf(address key) internal view returns (uint) {
		for (uint i = 0 ; i < keys.length ; i++) {
			if (keys[i] == key) {
				return i;
			}
		}
		require(false, "Could not find key"); // preparation for sanity feature
	}

	function iterate() external {
		for (uint i = 0 ; i < keys.length ; i++) {
			address key = keys[i];
			doSomething(key, get(key));
		}
	}

	function doSomething(address key, address value) virtual internal {}

}
