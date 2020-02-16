library SafeMath {
	function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

	function safeSub(uint256 x, uint256 y) internal returns(uint256) {
		assert(x >= y);
		uint256 z = x - y;
		return z;
    }
}



contract Bank {
    mapping (address => uint256) public funds;
	uint256 public totalFunds;

	
	

    function deposit(uint256 amount) public payable {
		require(msg.sender != address(0));
		funds[msg.sender] = funds[msg.sender].add(amount);
		totalFunds = totalFunds.add(amount);
    }

    function transfer(address to, uint256 amount) public {
		require(to!= address(0));
		require(funds[msg.sender] > amount);
		funds[msg.sender] = funds[msg.sender].sub(amount);
		funds[to] = funds[to].add(amount);
		
    }

    function withdraw() public returns (bool success)  {
		uint256 amount = getfunds(msg.sender);
		funds[msg.sender] = 0;
		success = msg.sender.send(amount);
		require(success);
		totalFunds = totalFunds.sub(amount);
    }
	
	function getfunds(address account) public returns (uint256) {
		return funds[account];
	}
	
	function getTotalFunds() public returns (uint256) {
		return totalFunds;
	}

	function init_state() public {}
}