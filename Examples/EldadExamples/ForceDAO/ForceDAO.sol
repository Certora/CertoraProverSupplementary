pragma solidity ^0.7.6;

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

import "ERC20.sol";

contract ForceDAO is ERC20 {
    uint public recorded_deposited_amount = 0;
    address pay_token;

    constructor (address _pay_token) public {
        pay_token = _pay_token;
    }

    function deposit(uint amount) public {
        iERC20(pay_token).transferFrom(msg.sender, address(this), amount);
        balances[msg.sender] += amount;
        total += amount;
        sync();
    }

    function withdraw(uint amount) public {
        require(amount <= balances[msg.sender]);
        iERC20(pay_token).transferFrom(address(this), msg.sender, amount);
        balances[msg.sender] -= amount;
        recorded_deposited_amount -= amount;
    }

    function sync() private {
        recorded_deposited_amount = iERC20(pay_token).balanceOf(address(this));
    }
}