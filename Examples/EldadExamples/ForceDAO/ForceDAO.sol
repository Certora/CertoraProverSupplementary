pragma solidity ^0.6.7;

/* 
    The vulnerability was that ForceDAO used ERC20 
    implementation (MiniMeToken) in which if a function
    call fails then returns false. 
    
    In most of ERC20 implementation the functin reverts 
    instead of returning false.

    The MiniMeToken fixed this issue in the following commit:
    https://github.com/Giveth/minime/commit/ea04d950eea153a04c51fa510b068b9dded390cb

    mint 1:1 ratio.
*/


contract ForceDAO is ERC20 {
    uint recorded_deposited_amount = 0;
    address pay_token;

    constructor (address _pay_token) {
        pay_token = _pay_token;
    }

    function deposit(uint amount) {
        transferFrom(msg.sender, address(this), amount);
        balances[msg.sender] += amount;
        sync();
    }

    function withdraw(uint amount) {
        require(amount < balances[msg.sender]);
        uint to_pay = amount * recorded_deposited_amount / totalSupply()
        iERC20(pay_token).transfer(msg.sender, to_pay);
    }

    function sync() {
        recorded_deposited_amount = iERC20(pay_token).balanceOf(address(this));
    }
}