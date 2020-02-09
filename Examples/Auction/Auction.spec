methods {
	// define methods of the contract that are independent of the environmnet 
	totalSupply() returns uint envfree
	owner() returns address envfree
	getAuction(uint)  returns uint,uint,address,uint,uint envfree
}
rule bounded_supply(method f) {
    env e;
	uint256 _supply = sinvoke totalSupply(); // total supply before
	require (_supply < 100000); //start with a reasonable amount

    // the next 3 lines invoke an arbitrary public function on an arbitrary input
    calldataarg arg;
    sinvoke f(e,arg);

    uint256 supply_ = sinvoke totalSupply(); // total supply after

    assert  supply_ < 115792089237316195423570985008687907853269984665640564039457584007913129639935,
           "Cannot increase to MAX_UINT256";
	
}

// once the bounded supply rule shows a case where the close function can cause an increase of the
// total supply to maxint, one can check what does it take to get to that situation  
rule full_scenario(uint id, uint payment, uint bidAmount) {
	uint256 _supply = sinvoke totalSupply(); // total supply before
	require (_supply < 100000); //start with a reasonable amount
	env eNew;
	sinvoke newAuction(eNew,id,payment);
	
	// get for info what are the fields of the generated auction
	uint _prize;
	uint _payment;
	address _winner;
	uint _bid_expiry;	
	uint _end_time;
	require (_prize,_payment,_winner,_bid_expiry,_end_time) == sinvoke getAuction(id);
	
	env eBid;
	// the interesting case is of a non privileged user
	require eBid.msg.sender != sinvoke owner();
	sinvoke bid(eBid,id,bidAmount);
	
	uint prize_;
	uint payment_;
	address winner_;
	uint bid_expiry_;	
	uint end_time_;
	require (prize_,payment_,winner_,bid_expiry_,end_time_) == sinvoke getAuction(id);

	// did anything change?
	if(_prize == prize_ && _payment==payment_ && _winner ==winner_ && _bid_expiry==bid_expiry_ && _end_time==end_time_) {
		assert false, "no need for the bid operation";
	}
	
	env eClose;
	//can the melicious user do the close? 
	require eBid.msg.sender == eBid.msg.sender;
	sinvoke close(eClose,id);
	uint256 supply_ = sinvoke totalSupply(); 

    assert  supply_ < 115792089237316195423570985008687907853269984665640564039457584007913129639935,
           "Cannot increase to MAX_UINT256";
	
}