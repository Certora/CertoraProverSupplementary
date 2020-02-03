contract Bank {
    mapping (address => uint256) public funds;
	uint256 public totalFunds;

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");

        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a, "SafeMath: subtraction overflow");
        uint256 c = a - b;

        return c;
    }
	
	

    function deposit(uint256 amount) public payable {
		require(msg.sender != address(0));
		funds[msg.sender] = add(funds[msg.sender],amount);
		totalFunds = add(totalFunds,amount);
    }

    function transfer(address to, uint256 amount) public {
		require(to!= address(0));
		require(funds[msg.sender] > amount);
		funds[msg.sender] =sub(funds[msg.sender],amount);
		funds[to] = add(funds[to],amount);
		
    }

    function withdraw() public returns (bool success)  {
		uint256 amount = getfunds(msg.sender);
		funds[msg.sender] = 0;
		success = msg.sender.send(amount);
		require(success);
		totalFunds = sub(totalFunds,amount);
    }
	
	function getfunds(address account) public returns (uint256) {
		return funds[account];
	}
	
	function getTotalFunds() public returns (uint256) {
		return totalFunds;
	}

	function init_state() public {}
}