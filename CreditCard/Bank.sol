pragma solidity ^0.8.7;

contract Bank {
    mapping(address => uint256) public funds;
    mapping(address => mapping(address => uint256)) allowences;
    uint256 public totalFunds;

    function getFunds(address account) public view returns (uint256) {
        return funds[account];
    }

    function getTotalFunds() public view returns (uint256) {
        return totalFunds;
    }

    function getEthBalance(address account) public view returns (uint256) {
        return account.balance;
    }

    function deposit(uint256 amount) public payable {
        require(msg.sender != address(0));
        require(msg.value == amount);
        funds[msg.sender] = funds[msg.sender] + amount;
        totalFunds = totalFunds + amount;
    }

    function getAllowence(address owner, address spender)
        public
        view
        returns (uint256)
    {
        return allowences[owner][spender];
    }

    function transfer(address to, uint256 amount) public {
        require(to != address(0));
        require(funds[msg.sender] > amount, "Bank: insufficient funds");
        funds[msg.sender] = funds[msg.sender] - amount;
        funds[to] = funds[to] + amount;
    }

    function transferFrom(
        address sender,
        address reciever,
        uint256 amount
    ) public {
        uint256 currentAllowance = allowences[sender][msg.sender];
        require(currentAllowance >= amount);
        unchecked {
            approve(sender, msg.sender, currentAllowance - amount);
        }

        _transfer(sender, reciever, amount);
    }

    function approve(address spender, uint256 amount) public {
        _approve(msg.sender, spender, amount);
    }

    function withdraw(uint256 amount) public returns (bool success) {
        require(amount <= getFunds(msg.sender));
        funds[msg.sender] -= amount;
        success = payable(msg.sender).send(amount);
        require(success);
        totalFunds = totalFunds -= amount;
    }

    function _transfer(
        address sender,
        address reciever,
        uint256 amount
    ) internal {
        require(sender != address(0));
        require(reciever != address(0));
        uint256 senderBalance = funds[sender];
        require(senderBalance >= amount);
        funds[sender] = senderBalance - amount;
        funds[reciever] += amount;
    }

    function _approve(
        address owner,
        address spender,
        uint256 amount
    ) internal {
        require(owner != address(0));
        require(spender != address(0));

        allowences[owner][spender] = amount;
    }
}
