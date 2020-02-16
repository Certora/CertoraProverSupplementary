//file bank.spec
pragma specify 0.1
methods {
    init_state()
    getfunds(address) returns uint256 envfree
	getTotalFunds()  returns uint256 envfree
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
   // invoke function transfer and assume - caller is e.msg.from
   uint256 balance = invoke getfunds(e.msg.sender);
   invoke transfer(e,to,amount);
   // check that transfer reverts if not enough funds
   assert balance < amount => lastReverted , "not enough funds";
}

rule others_can_only_increase(address other, method f) {
   env e;
   
   //assume msg.sender is a different address
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

rule can_withdraw_after_any_time_and_any_other_transaction(method f) {	
	address account;
	uint256 amount;
	
	// account deposits amount 
	env _e;
	require _e.msg.sender == account;
	require amount > 0;
	sinvoke deposit(_e,amount);
	
	//any other transaction beside withdraw by account
	env eF;
	require (f.selector != withdraw().selector && f.selector!=transfer(address, uint256).selector) || eF.msg.sender!=account;
	calldataarg arg; // any argument
	sinvoke f(eF,arg); // successful (potentially state-changing!)
   
	//account withdraws
	env e_;
	require e_.block.timestamp > _e.block.timestamp ; // The operation occurred after the initial operation
	require e_.msg.sender == account;
	sinvoke withdraw(e_);
	// check the erc balnce 
	uint256 ercBalance = sinvoke _ercBalance(e_);
	assert ercBalance >= amount, "should have at least what have been deposited";
	

}



rule additiveTransfer {
	env e1; 
	env e2;
	uint256 a;
	uint256 b;
	address to;
	address from;
	uint256 balanceToCase1;
	uint256 balanceToCase2;
	uint256 balanceFromCase1;
	uint256 balanceFromCase2;
	  
	storage init = lastStorage; // record state before the transaction

	require(e1.msg.sender == from) && (e2.msg.sender==from); // e1 and e2 transfer from the same address from
		
	//transfer a and then b from form 'from' to 'to'
	sinvoke transfer(e1,to,a);
	sinvoke transfer(e2,to,b);
	balanceToCase1 = sinvoke getfunds(to);
	balanceFromCase1 = sinvoke getfunds(from);
    // start a new transaction
	sinvoke transfer(e1, to, a+b) at init ;
	balanceToCase2 = sinvoke getfunds(to);
	balanceFromCase2 = sinvoke getfunds(from);
	assert balanceToCase1 == balanceToCase2 && balanceFromCase1==balanceFromCase2, "expected transfer to be additive" ;
}