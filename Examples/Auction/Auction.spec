/* Certora prover verifies calls for all environments. The environment is passed an additional parameter to functions.
It can be seen as the following:
struct env {
    address msg.address // address of the contract begin verified
    address msg.sender //  sender of the message 
    uint msg.value  // number of wei sent with the message
    uint block.number // current block number
    uint block.timestamp // current time stamp
    address tx.origin // original message sender
}

*/

/**************** Generic rules ***********************/
//A rule for verifying that any scenario proferemed by some sender does not decrease the balance of any other account.
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
transferWithIllegalValue(address to)
{
    env e; // for every possible environment
    require to != 0; //assume the case that address to in not zero

    require e.msg.value == 0; //assume no msg.value since this is not a payable function
    bool res = invoke transferTo(e, to, 0);

    assert lastReverted || !res, "permits a transfer of zero tokens";
}



// A rule for verifying  that the total supply is always less than  max_int
rule boundedSupplyDelta(method f) {
    env e; //for every possible environment 
    uint delta = 115792089237316195423570985008;
    uint256 _supply = sinvoke totalSupply(e); // total supply before
	//start with a reasonable amount
	//if we are already close to max_int than in one operation it is feasible to reach max_int
	
    // invoke an arbitrary public function on an arbitrary input and take into account only cases that do not revert
    calldataarg arg;
    sinvoke f(e,arg);

    uint256 supply_ = sinvoke totalSupply(e); // total supply after

    assert  supply_ < _supply + delta, "Cannot increase to MAX_UINT256";
    
}


// A rule for verifying  that the total supply is always less than  max_int
rule boundedSupply(method f) {
    env e; //for every possible environment 
    uint256 _supply = sinvoke totalSupply(e); // total supply before
	//start with a reasonable amount
	//if we are already close to max_int than in one operation it is feasible to reach max_int
	require(_supply < 10000000);
    // invoke an arbitrary public function on an arbitrary input and take into account only cases that do not revert
    calldataarg arg;
    sinvoke f(e,arg);

    uint256 supply_ = sinvoke totalSupply(e); // total supply after

    assert  supply_ <115792089237316195423570985008687907853269984665640564039457584007913129639935, "Cannot increase to MAX_UINT256";
    
}

/************** A specific rule **********************/
// once the bounded supply rule shows a case where the close function can cause an increase of the
// total supply to maxint, one can check what does it take to get to that situation  
// this is a generalized unit test

rule fullScenario(uint id, uint payment, uint bidAmount, uint start) {
    env eNew;
    uint256 _supply = sinvoke totalSupply(eNew); // total supply before
    //the signature of newAuctoin has changed so choose the right one
	sinvoke newAuction(eNew,id,payment); //orig version
	
    
    // get what are the fields of the generated auction
    uint _prize;
    uint _payment;
    address _winner;
    uint _bid_expiry;    
    uint _end_time;
    require (_prize,_payment,_winner,_bid_expiry,_end_time) == sinvoke getAuction(eNew,id);
    
    env eBid;
    // the interesting case is of a non privileged user
    require eBid.msg.sender != sinvoke owner(eBid);
    sinvoke bid(eBid,id,bidAmount);
    
    uint prize_;
    uint payment_;
    address winner_;
    uint bid_expiry_;    
    uint end_time_;
    require (prize_,payment_,winner_,bid_expiry_,end_time_) == sinvoke getAuction(eBid,id);

    // did anything change?
    if(_prize == prize_ && _payment==payment_ && _winner ==winner_ && _bid_expiry==bid_expiry_ && _end_time==end_time_) {
        assert false, "no need for the bid operation";
    }
    
    env eClose;
    //can the malicious user do the close? 
    require eBid.msg.sender == eBid.msg.sender;
    sinvoke close(eClose,id);
    uint256 supply_ = sinvoke totalSupply(eClose); 

    assert  supply_ < 115792089237316195423570985008687907853269984665640564039457584007913129639936,
           "Cannot increase to MAX_UINT256";
    
}
