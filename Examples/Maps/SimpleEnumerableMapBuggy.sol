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
		// buggy impl
		if (map[key] == address(0)) {
			map[key] = value;
			keys.push(key);
		}
	}

	function remove(address key) external {
		// buggy: what happens if we remove a key that does not exist?
		map[key] = address(0);
		uint i = indexOf(key);
		if (i == keys.length - 1) {
			keys.pop();
		} else {
			keys[i] = keys[keys.length-1];
			keys.pop();
		}
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
