library SafeMath {
	function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

	function safeSub(uint256 x, uint256 y) internal pure returns(uint256) {
		assert(x >= y);
		uint256 z = x - y;
		return z;
    }
}

contract Bank {
	using SafeMath for uint256;
	
	// the balance a user has in the bank
	mapping (address => uint256) private funds;

	// a user becomes active when depositing. She becomes inactive when withdrawing or transfing the whole balance  
	mapping (address => bool) private active;
	
	function deposit(uint256 amount) public payable {
		require(amount > 0 && amount == msg.value);
		funds[msg.sender] = funds[msg.sender].safeAdd(amount);
		active[msg.sender] = true;
	}
	
	function transfer(address to, uint256 amount) public {
		require(amount > 0 && funds[msg.sender] > amount );
		active[to] = true;
		if (funds[msg.sender] == amount)  {
			active[msg.sender] = false;
		}
		funds[msg.sender] = funds[msg.sender].safeSub(amount);
		funds[to] = funds[to].safeAdd(amount);
	}
	
	function withdraw() public returns (bool success)  {
		uint256 amount = getFunds(msg.sender);
		funds[msg.sender] = 0;
		success = msg.sender.send(amount);
		require(success);
		active[msg.sender] = false;
	}
	
	function getFunds(address account) public view returns (uint256) {
		require (active[account]);
		return funds[account];
	}
	
	function isActive(address account) public view returns (bool) {
		return active[account];
	}

	function init_state() public {}

	function getEthBalance(address account) public view returns (uint256){
		return account.balance;
	}
}