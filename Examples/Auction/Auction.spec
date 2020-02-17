

/* Certora prover verifies calls for all environments. The environment is passed an additional parameter to functions.
It can be seen as the following:
struct env {
    address msg.address // address of the contract begin verified
    address msg.sender // sender of the message 
    uint msg.value // number of wei sent with the message
    uint block.number // current block number
    uint block.timestamp // current time stamp
    address tx.origin // original message sender
}

*/

/**************** Generic rules ***********************/
// A rule for verifying that the total supply stays less than max_int
rule boundedSupply(method f) {
    env e; //for every possible environment 
    uint256 _supply = sinvoke totalSupply(e); // total supply before
	
	// invoke an arbitrary public function on an arbitrary input and take into account only cases that do not revert
    calldataarg arg;
    sinvoke f(e,arg);

    uint256 supply_ = sinvoke totalSupply(e); // total supply after

    assert _supply != supply_ => supply_ <115792089237316195423570985008687907853269984665640564039457584007913129639935, "Cannot increase to MAX_UINT256";
    
}

//A rule for verifying that any scenario preformed by some sender does not decrease the balance of any other account.
rule senderCanOnlyIncreaseOthersBalance( method f, address sender, address other)
{
env e;//for every possible environment 
    require other != sender; //assume we have two different accounts.
    uint256 origBalanceOfOther = sinvoke balanceOf(e, other); //get the current balance of the other account

    //invoke any function with msg.sender the sender account
    calldataarg arg;
    env ef;
    require ef.msg.sender == sender;
    invoke f(ef, arg);

    env e2;
    uint256 newBalanceOfOther = sinvoke balanceOf(e2, other);

    assert newBalanceOfOther >= origBalanceOfOther, "The balance of other account decreased"; 
}

//A rule for verifying a correct behavior on sending zero tokens - return false or revert 
rule transferWithIllegalValue(address to)
{
    env e; // for every possible environment
    require to != 0; //assume the case that address to in not zero

    require e.msg.value == 0; //assume no msg.value since this is not a payable function
    bool res = invoke transferTo(e, to, 0);

    assert lastReverted || !res, "permits a transfer of zero tokens";
}




