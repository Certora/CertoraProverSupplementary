contract BOG {
    uint _burnRatio = 1; // 5%
    uint _distributeRatio = 4; // 80% distributed

    // contract status
    uint total_fees = 0;
    uint total_supply = 75 ether;

    // user status
    struct UserInfo {
        uint fessCollected; // the total fees per share that has been already collected  -TODO chage name PerShare
    }

    mapping (address => UserInfo) accounts;
    mapping (address => uint) balances;
    
    constructor() payable {
        require(msg.value == 75 ether);
        balances[address(this)] = total_supply;
    }


    function _burn(address account, uint amount) private {
        balances[account] -= amount;
        total_supply -= amount;
    }

    function _distribute(address account, uint amount) private {
        total_fees += amount;
    }

    function upadateResults(address account) private {
        uint reward = (balances[account] / total_supply) * (total_fees - accounts[account].fessCollected);
        balances[account] += reward;
        accounts[account].fessCollected = total_fees;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public {
        upadateResults(sender);
        upadateResults(recipient);

        uint256 toBurn = amount * _burnRatio / 100; // calculate amount to burn
        uint256 toDistribute = amount * _distributeRatio / 100; // calculate amount to distribute
        _burn(sender, toBurn);
        _distribute(sender, toDistribute);
        
        amount = amount - toBurn - toDistribute;
        balances[sender] -= amount;
        balances[recipient] += amount;        
    }

    function transfer(address recipient, uint256 amount) public {
        transferFrom(msg.sender, recipient, amount);
    }
    
    function buyTokens() public payable {
        require(balances[address(this)] >= msg.value);
        
        balances[msg.sender] += msg.value;
        balances[address(this)] -= msg.value;
    }
    
    function sellAllTokens() public {
        uint to_pay = myBalance() + myGainedFees();
        balances[msg.sender] = 0;
        msg.sender.call{value: to_pay}("");
    }
    
    function myBalance() view public returns(uint) {
        return balances[msg.sender];
    }
    
    function myGainedFees() view public returns(uint) {
        return total_fees * balances[msg.sender] / total_supply;
    }
    
    function myWorth()  view public returns(uint) {
        return myBalance() + myGainedFees();
    }
}   