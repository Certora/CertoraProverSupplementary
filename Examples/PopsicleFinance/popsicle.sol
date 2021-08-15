pragma solidity ^0.8.4;
/* 
    The popsicle finance platform is used by pools liquidity providers to maximize their fees gain from providing liquidity to pools. 
*/



contract PopsicleFinance {
    address owner;
    uint share_price = 1 ether;

    event CreateUser(address user_address, uint current_number_of_accounts);
    event Deposit(address user_address, uint deposit_amount);
    event Withdraw(address user_address, uint withdraw_amount);
    event TransferShares(address _from, address _to, uint amount_of_shares);
    event CollectReward(address collector, uint gain);
    event PositiveGain(address user_address, uint this_time_gain_per_share, uint total_gain_per_share);
    
    struct UserInfo {
        uint shares_number; // the amount of shares this user holds.
        uint profit_gained_per_share; // the amount of fees earned for this share and not collected yet. 
    }
    
    // accounts data
    mapping (address => UserInfo) accounts;
    mapping (address => bool) accounts_initialized;
    mapping (uint=>address) accounts_list;
    uint accounts_number = 0;
    
    constructor() {
        owner = msg.sender;
    }
    
    function deposit(uint shares_amount_to_buy) public payable {
        // if the account doesn't exists - create a new account
        if (!accounts_initialized[msg.sender]) {
            accounts[msg.sender] = UserInfo(0, 0);
            accounts_initialized[msg.sender] = true;
            accounts_list[accounts_number] = msg.sender;
            accounts_number += 1;
            emit CreateUser(msg.sender, accounts_number);
        }
        
        // execute the deposit
        require(msg.value >= shares_amount_to_buy * share_price);
        uint new_shares_number = accounts[msg.sender].shares_number + shares_amount_to_buy;
        uint new_profit_gained_per_share = (accounts[msg.sender].shares_number * accounts[msg.sender].profit_gained_per_share) / new_shares_number;
        accounts[msg.sender].shares_number = new_shares_number;
        accounts[msg.sender].profit_gained_per_share = new_profit_gained_per_share;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint shares_amount_to_withdraw) public {
        require(accounts_initialized[msg.sender]);
        require(accounts[msg.sender].shares_number >= shares_amount_to_withdraw);
        accounts[msg.sender].shares_number -= shares_amount_to_withdraw;
        uint withdraw_amount = shares_amount_to_withdraw * share_price;
        msg.sender.call{value: withdraw_amount}("");
        emit Deposit(msg.sender, withdraw_amount);
    }

    /* 
        the vulnerability - this method doesn't transfer the user gain_per_share when users transfer their shares. 
        This way a user that claimed its reward can transfer its shares to another user that will claim again the profit of the same share. 
    */ 
    function transfer_shares(uint number_of_shares_to_transfer, address to_account) public {
        require(accounts_initialized[msg.sender]);
        require(accounts_initialized[to_account]);
        require(accounts[msg.sender].shares_number >= number_of_shares_to_transfer);
  
        accounts[msg.sender].shares_number -= number_of_shares_to_transfer;
        accounts[to_account].shares_number += number_of_shares_to_transfer;
        
        /*  
            To fix the bug we should also consider the _from and _to gain_per_share values.
            accounts[to_account].profit_gained_per_share = (accounts[to_account].profit_gained_per_share * accounts[to_account].shares_number 
                                                           + accounts[from_account].profit_gained_per_share * number_of_shares_to_transfer) / 
                                                           (accounts[to_account].shares_number + number_of_shares_to_transfer)
                                                           
            accounts[from_account], accounts[to_account] values refer to the values at the begining of the execution.
                                                           
        */
        emit TransferShares(msg.sender, to_account, number_of_shares_to_transfer);
    }
    
    
    /* 
        This function allows a user to collect its accumelated fees (send them to its wallet).
        At the meanwhile those fees aren't reinvested. 
    */
    function collect_reward() public {
        require(accounts_initialized[msg.sender]);
        require(accounts[msg.sender].profit_gained_per_share >= 0);
        uint tmp_profit_gained_per_share = accounts[msg.sender].profit_gained_per_share;
        accounts[msg.sender].profit_gained_per_share = 0;
        uint reward = accounts[msg.sender].shares_number * tmp_profit_gained_per_share;
        msg.sender.call{value: reward}("");
        emit CollectReward(msg.sender, reward);
    }

    
    /* 
        This function adds a contant gain for every share. 
        This are the fees that charged from the pools popsicle finance is a liquidity provider of. 
        Without this function there is no vulnerability 
    */
    function add_gain_per_share() public payable {
        // require(msg.sender == owner);
        for (uint i=0; i<accounts_number; i++) {
            address acc_addreess = accounts_list[i];
            accounts[acc_addreess].profit_gained_per_share += 1 ether; 
            emit PositiveGain(msg.sender, 1 ether, accounts[acc_addreess].profit_gained_per_share);
        }   
    }
    
    
    
    // This function is to allow the share price to change, something the attacker can also profit from. 
    function increase_share_price() public payable {
        require(msg.sender == owner);
        share_price += 1 ether;
    }
    
    // This function is to allow the share price to change, something the attacker can also profit from.
    function decrease_share_price() public payable {
        require(msg.sender == owner);
        share_price -= 1 ether;
    }
    
    // Return the current share price
    function get_share_price() public view returns(uint) {
        return share_price;
    }
    
    // Return the number of shares hold by the function caller (msg.sender)
    function get_number_of_shares() public view returns(uint) {
        require(accounts_initialized[msg.sender]);
        return accounts[msg.sender].shares_number;
    }
    
    // Return the rewards of msg.sender
    function show_gain_per_share() public view returns(uint){
        require(accounts_initialized[msg.sender]);
        return accounts[msg.sender].profit_gained_per_share;
    }



}