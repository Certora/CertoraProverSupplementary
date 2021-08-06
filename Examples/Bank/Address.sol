pragma solidity >= 0.4.24 < 0.8;

contract Address {
    // balance of the Address in Wei
    function balance(address a) public returns (uint256) {
        return a.balance;
    }

    // send given amount of Wei to Address, reverts on failure, forwards 2300 gas stipend, not adjustable
    function transfer(address payable a, uint256 amount) public {
        return a.transfer(amount);
    }

    // send given amount of Wei to Address, returns false on failure, forwards 2300 gas stipend, not adjustable
    function send(address payable a, uint256 amount) public returns (bool) {
        return a.send(amount);
    }

    // issue low-level CALL with the given payload, returns success condition and return data, forwards all available gas, adjustable
    function call(address a, bytes memory mem) public returns (bool, bytes memory) {
        return a.call(mem);
    }

    // issue low-level DELEGATECALL with the given payload, returns success condition and return data, forwards all available gas, adjustable
    function delegatecall(address a, bytes memory mem) public returns (bool, bytes memory) {
        return a.delegatecall(mem);
    }

    // issue low-level STATICCALL with the given payload, returns success condition and return data, forwards all available gas, adjustable 
    function staticcall(address a, bytes memory mem) public returns (bool, bytes memory) {
        return a.staticcall(mem);
    }
}