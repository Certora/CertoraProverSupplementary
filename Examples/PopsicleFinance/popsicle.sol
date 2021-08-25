pragma solidity ^0.8.4;
/* 
    The popsicle finance platform is used by pools liquidity providers to maximize their fees gain from providing liquidity to pools. 
*/

import "./ERC20.sol";



contract PopsicleFinance is ERC20 {
    event Deposit(address user_address, uint deposit_amount);
    event Withdraw(address user_address, uint withdraw_amount);
    event CollectFees(address collector, uint totalCollected);
    
    
    address owner;
    uint totalFeesEarned = 0; // total fees earned per share

    mapping (address => UserInfo) accounts;
    
    constructor() {
        owner = msg.sender;
    }
    
    struct UserInfo {
        uint fessCollected; // the total fees per share that has been already collected  -TODO chage name PerShare
        uint Rewards; // general "debt" of popsicle to the user 
    }

    function deposit() public payable {
        uint amount = msg.value;
        uint reward = balances[msg.sender] * (totalFeesEarned - accounts[msg.sender].fessCollected);
        accounts[msg.sender].fessCollected = totalFeesEarned;
        accounts[msg.sender].Rewards += reward;
        mint(msg.sender, amount);
        emit Deposit(msg.sender, amount);
    }


    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount);
        uint reward = amount * (totalFeesEarned - accounts[msg.sender].fessCollected);
        burn(msg.sender, amount);
        accounts[msg.sender].Rewards += reward;
        emit Withdraw(msg.sender, amount);
    }

    function collectFees() public {
        require(totalFeesEarned >= accounts[msg.sender].fessCollected);
        uint fee_per_share = totalFeesEarned - accounts[msg.sender].fessCollected;  
        uint to_pay = fee_per_share * balances[msg.sender] + accounts[msg.sender].Rewards;
        accounts[msg.sender].fessCollected = totalFeesEarned;
        accounts[msg.sender].Rewards = 0;
        msg.sender.call{value: to_pay}("");
        emit CollectFees(msg.sender, to_pay);
    }
    
    function OwnerDoItsJobAndEarnsFeesToItsClients() public payable {
        totalFeesEarned += 1;
    }


    // added for spec
    function assetsOf(address user) public view returns(uint) {
        return accounts[msg.sender].Rewards + balances[user] * (totalFeesEarned - accounts[msg.sender].fessCollected);
    }
}