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

rule can_withdraw_after_any_time_and_any_other_transaction() {	
	address account;
	uint256 amount;
	method f;
	
	// account deposits amount 
	env _e;
	require _e.msg.sender == account;
	require amount > 0;
	sinvoke deposit(_e,amount);
	
	//any other trasaction beside withdraw by account
	env eF;
	require (f != withdraw && f!=transfer) || eF.msg.sender!=account;
	calldataarg arg; // any argument
	sinvoke f(eF,arg); // successful (potentially state-changing!)
   
	//account withdraws
	env e_;
	require e_.block.timestamp > _e.block.timestamp ; // The operation occured after the initial operation
	require e_.msg.sender == account;
	sinvoke withdraw(e_);
	// check the erc balnce 
	uint256 ercBalance = sinvoke _ercBalance(e_);
	assert ercBalance >= amount, "should have at least what have been deposisted";
	

}


/*
rule inverseTransfer(address account1, address account2,uint amount) {

	storage init = lastStorage;
	
	env e_a1; 
	env e_a2;
	require amount > 0;
	require(e_a1.msg.sender == account1);
	require(e_a2.msg.sender == account2);
	
	//transfer form account1 to account2 and back
	sinvoke transfer(e_a1,account2,amount);
	sinvoke transfer(e_a2,account1,amount);
	balanceAccount1Case1 = sinvoke getfunds(account1);
	balanceAccount2Case1 = sinvoke getfunds(account2);
	
	
	
	sinvoke transfer(e_a1,account1,amount) at init;
	sinvoke transfer(e_a2,account1,amount);

}
*/