//file bank.spec
pragma specify 0.1
methods {
    init_state()
    getfunds(address) returns uint256 envfree
}

invariant address_zero_cannot_become_an_account(env e,address z) z==0 => sinvoke getfunds(z)==0

rule withdraw_succeeds {
   env e; // env represents the bytecode environment passed one every call
   // invoke function withdraw and assume that it does not revert
   bool success = sinvoke withdraw(e);  // e is passed as an additional arg
   assert success,"withdraw must succeed"; // verify that withdraw succeed
}

rule transfer_reverts(address to, uint256 amount) {
   env e;
   // invoke function transfer and assume - caller is w.msg.from
   uint256 balance = invoke getfunds(e.msg.sender);
   invoke transfer(e,to,amount);
   // check that transfer reverts if not enough funds
   assert balance < amount => lastReverted , "not enough funds";
}

rule others_can_only_increase() {
   env e;
   address other;
   method f;
   //assume msg.sender is a different addres
   require e.msg.sender != other;
   //get balance before
   uint256 _balance = sinvoke getfunds(other);
   // exec some method
   calldataarg arg; // any argument
   sinvoke f(e,arg); // successful (potentially state-changing!)
   //get blance after
   uint256 balance_ = sinvoke getfunds(other);
   //balance should not be reduce by any operation
   //can increase due to a transfer to msg.sender
   assert _balance <= balance_ ,"withdraw from others balance";
}
