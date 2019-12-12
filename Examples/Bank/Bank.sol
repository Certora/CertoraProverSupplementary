contract Bank {
    mapping (address => uint256) public funds;

    function deposit(uint256 amount) public payable {
		funds[msg.sender] += amount;
    }

    function transfer(address to, uint256 amount) public {
		require(funds[msg.sender] > amount);
		funds[msg.sender] -= amount;
		funds[to] += amount;
    }

    function withdraw() public returns (bool success)  {
		uint256 amount = funds[msg.sender];
		funds[msg.sender] = 0;
		success = msg.sender.send(amount);
    }
	
	function getfunds(address account) public returns (uint256) {
		return funds[account];
	}

	function init_state() public {}
}