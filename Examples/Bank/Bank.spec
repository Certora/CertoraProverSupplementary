 pragma specify 0.1
methods {
	getFunds(address) returns uint256 envfree
	getTotalFunds() returns uint256 envfree
	getEthBalance(address) returns uint256 envfree
}

/* Invoke the withdraw method and assume that it does not revert.
   Then make sure that withdraw returns `success == true`.
 */
rule withdraw_succeeds {
	/* The env type represents the EVM parameters passed in every 
	   call (msg.*, tx.*, block.* variables in solidity 
	 */
	env e; 
	// Invoke function withdraw and assume it does not revert
	/* For non-envfree methods, the environment is passed as the first argument*/
	bool success = withdraw(e);
	assert success, "withdraw must succeed";
}

/* This rule checks that actions executed by a certain actor
   can only positively impact other addresses.
   Here, an action invoked by `e.msg.sender` can only increase the 
   balance of another address `other`.
 */
rule others_can_only_increase_my_balance() {
	method f; // an arbitrary function in the contract
	env e;  // the execution environment

	address other;
	// Assume the actor and the other address are distinct
	require e.msg.sender != other;

	// Get the balance of `other` before the invocation
	uint256 _balance = getFunds(other);
	
	calldataarg arg; // any argument
	f(e, arg); // successful (potentially state-changing!)
	
	// Get the balance of `other` after the invocation
	uint256 balance_ = getFunds(other);
	
	assert _balance <= balance_, "Reduced the balance of another address";
}

/* The zero address must not hold funds. */
invariant address_zero_cannot_become_an_account() 
	getFunds(0) == 0


/* Invoke the transfer method where caller is `e.msg.sender`.
   Check that the invoke reverts if caller does not have enough funds.
 */
rule transfer_reverts(address to, uint256 amount) {
	env e;
	// Get the caller's balance before the invocation of transfer
	uint256 balance = getFunds(e.msg.sender);
	invoke transfer(e,to,amount);
	assert balance < amount => lastReverted , "not enough funds";
}

/* The rule checks that after a successful deposit by an account, 
   and the invocation of an arbitrary function by any actor*, 
   the subsequent invocation of the withdraw method will lead
   to a state where the Ether balance of the account will be at least
   the amount initially deposited.
   *the exception to the rule is whether withdraw occurs earlier,
	or if the actor sends out the funds (to potentially another address).
 */
rule can_withdraw_after_any_time_and_any_other_transaction(method f) {
	// Choose arbitrary account and amount.
	// (This is the same as declaring those in the rule header.)
	address account;
	uint256 amount;
	
	// `account` deposits `amount`
	env _e;
	require _e.msg.sender == account &&
			amount > 0;
	deposit(_e,amount);
	
	// any other transaction beside withdraw by account, or transfer by the account
	env eF;
	require f.selector != withdraw().selector && 
			(eF.msg.sender == account => 
				f.selector != transfer(address,uint256).selector);
	calldataarg arg; // any argument
	f(eF,arg); // successful (potentially state-changing!)
   
	//account withdraws
	env e_;
	// withdraw is after f which is after deposit
	require e_.block.timestamp >= eF.block.timestamp && 
			e_.block.number >= eF.block.number && 
			eF.block.timestamp >= _e.block.timestamp && 
			eF.block.number >= _e.block.number; 
	require e_.msg.sender == account; // same account that deposited
	withdraw(e_);
	
	// check the Ether balance 
	uint256 ethBalance = getEthBalance(account);
	assert ethBalance >= amount, "should have been at least what has been deposited";
}

/* This rule examines two different executions involving `transfer`
   and shows that they are equivalent in their effect on the balances 
   `from` and `to`.
 */
rule additiveTransfer(uint256 amt1, uint256 amt2, address from, address to) {
	env e1; 
	env e2;

	// e1 and e2 transfer from the same address `from`
	require e1.msg.sender == from && e2.msg.sender == from; 
	
	// record state before the transaction
	storage init = lastStorage; 
		
	// Transfer amt1 and then amt2 from `from` to `to`
	transfer(e1,to,amt1);
	transfer(e2,to,amt2);
	uint256 balanceToCase1 = getFunds(to);
	uint256 balanceFromCase1 = getFunds(from);
	
	// Start a new transaction from the initial state
	uint256 sum_amt = amt1+amt2;
	transfer(e1, to, sum_amt) at init;
	uint256 balanceToCase2 = getFunds(to);
	uint256 balanceFromCase2 = getFunds(from);
	assert balanceToCase1 == balanceToCase2 && 
		   balanceFromCase1 == balanceFromCase2, 
		   "expected transfer to be additive" ;
}