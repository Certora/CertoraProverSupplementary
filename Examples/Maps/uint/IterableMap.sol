contract IterableMap {
	mapping(uint => uint) internal map;
	function get(uint key) public view returns(uint) { return map[key]; }

	uint[] internal keys;
	function numOfKeys() external view returns (uint) { return keys.length; }
	
	function insert(uint key, uint value) external {
		require(value != 0, "0 is not a valid value");
		require (!contains(key), "key already exists");
		map[key] = value;
		keys.push(key);
	}

	function remove(uint key) external {
		require (contains(key), "Key does not exist");
		map[key] = 0;
		uint i = indexOf(key);
		if (i < keys.length - 1) {
			keys[i] = keys[keys.length-1];
		}
		keys.pop();
	}

	function contains(uint key) public view returns (bool) {
		if (map[key] == 0) {
			return false;
		}
	
		return true;
	}

	function indexOf(uint key) internal view returns (uint) {
		for (uint i = 0 ; i < keys.length ; i++) {
			if (keys[i] == key) {
				return i;
			}
		}
		require(false, "Could not find key");
	}

    function iterate() external {
		for (uint i = 0 ; i < keys.length ; i++) {
			uint key = keys[i];
			doSomething(key, get(key));
		}
	}

	function doSomething(uint key, uint value) virtual public {
		map[key] = 100;
	}
}