pragma solidity ^0.8.7;
import "./Bank.sol";


contract CreditCard{

    mapping(uint256 => Bank) banks;
    address owner;
    modifier onlyOwner{
        require(owner == msg.sender, "not your credit card, back off");
        _;
    }
    constructor(){
        owner = msg.sender;
    }

    function pay(Bank senderBank, Bank recipientBank, address recipient, uint256 amount) public payable onlyOwner{
        require(senderBank.getAllowence(msg.sender)>=amount, "Please allow the credit to transfer the funds");
        senderBank.transferFrom(msg.sender, address(this), amount);
        senderBank.withdraw(amount);
        recipientBank.deposit(amount);
        recipientBank.transfer(recipient, amount);
    }
}