contract Bank {
    mapping (address => uint256) private funds;
	uint256  totalFunds;

    function deposit(uint256 amount) public payable {
		funds[msg.sender] += amount;
		totalFunds += amount;
    }

    function transfer(address to, uint256 amount) public {
		require(funds[msg.sender] > amount);
		uint256 fundsTo = funds[to];
		funds[msg.sender] -= amount;
		funds[to] = fundsTo + amount;		
    }

    function withdraw() public returns (bool success)  {
		uint256 amount = getFunds(msg.sender);
		funds[msg.sender] = 0;
		success = msg.sender.send(amount);
		totalFunds -=amount;
    }
	
	function getFunds(address account) public view returns (uint256) {
		return funds[account];
	}
	
	function getTotalFunds() public view returns (uint256) {
		return totalFunds;
	}

	function init_state() public {}
	
	function getEthBalance(address account) public view returns (uint256){
		return account.balance;
	}
}
