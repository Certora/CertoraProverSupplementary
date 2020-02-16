

rule bounded_supply(method f) {
    env e; //for every possible environment 
    uint256 _supply = sinvoke totalSupply(e); // total supply before
    require (_supply < 100000); //start with a reasonable amount

    // invoke an arbitrary public function on an arbitrary input and take into account only cases that do not revert
    calldataarg arg;
    sinvoke f(e,arg);

    uint256 supply_ = sinvoke totalSupply(e); // total supply after

    assert  supply_ < 115792089237316195423570985008687907853269984665640564039457584007913129639935,
           "Cannot increase to MAX_UINT256";
    
}

rule auctionPrizeOnlyReduces(uint256 id,method f) 
{
    env e;
    uint256 _prize;
    require (_prize,_,_,_,_ == sinvoke getAuction(e,id));

    calldataarg arg;
    sinvoke f(e,arg);

    uint256 prize_;
    require (prize_ ,_,_,_,_ == sinvoke getAuction(e,id));
    
    assert( prize_ <= _prize);
    
}
