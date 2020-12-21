/**
		Specification file for Certora Prover 

		
		In order to simulate the execution of all functions in the main contract, 
		you can define a method argument in the rule and use it in a statement.

		Run:
		 	certoraRun BankFixed.sol:Bank --verify Bank:Parametric.spec
		
		It discover an issue in transfer.
		Run also:
		 	certoraRun Bank.sol:Bank --verify Bank:Parametric.spec
		See that this rule also uncover the issue detected by integirty of deposit.
		

**/


rule validityOfTotalFunds(method f) {
	env e; 
	
	require  getTotalFunds(e) >= getFunds(e, e.msg.sender);
	
	// execute some method
   	calldataarg arg; // any argument
	f(e, arg);
	
	assert ( getTotalFunds(e) >= getFunds(e, e.msg.sender), "Total funds are less than user funds" );
}


// Adding local variables can help understanding counter example
rule validityOfTotalFundsWithVars(method f) {
	env e; 
	address account = e.msg.sender;
	
	uint256 userFundsBefore = getFunds(e, account);
	uint256 totalBefore = getTotalFunds(e);

	require totalBefore >= userFundsBefore;
	
	// execute some method
   	calldataarg arg; // any argument
	sinvoke f(e, arg); // simulate only non reverting paths 

	uint256 userFundsAfter = getFunds(e, account);
	uint256 totalAfter = getTotalFunds(e);
	
	assert ( totalAfter >= userFundsAfter, "Total funds are less than user funds" );
}
