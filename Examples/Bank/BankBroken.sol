pragma solidity >= 0.4.24 < 0.8;

contract Bank {
    mapping (address => uint256) public funds;
    uint256 public totalFunds;

    // get the current fund of an account
    function getFunds(address account) public view returns (uint256) {
        return funds[account];
    }

    // get the total funds in the bank
    function getTotalFunds() public view returns (uint256) {
        return totalFunds;
    }

    // deposit an amount to an account
    function deposit(uint256 amount) public payable {
        funds[msg.sender] += amount;
        totalFunds += amount;
    }

    // transfer an amount to an account
    function transfer(address to, uint256 amount) public {
        require(funds[msg.sender] > amount);
        funds[msg.sender] -= amount;
        funds[to] += amount;
    }

    // withdraw all amounts
    function withdraw() public returns (bool success)  {
        uint256 amount = getFunds(msg.sender);
        funds[msg.sender] = 0;
        success = msg.sender.send(amount);
        totalFunds -=amount;
    }

    function getEthBalance(address account) public view returns (uint256){
        return account.balance;
    }
}
