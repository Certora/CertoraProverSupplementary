/**
			Specification file for Certora Prover 

		
		In order to simulate the execution of all functions in the main contract, 
		you can define a method argument in the rule and use it in a statement.

		Run:
		 	certoraRun Bank.sol:Bank --verify Bank:Parametric.spec
		See how many issues this rules detects.

		Are they all fixed?
		 	certoraRun BankFixed.sol:Bank --verify Bank:Parametric.spec
		

**/


rule validityOfTotalFunds(method f) {
	env e; 
	
	require  getTotalFunds(e) >= getFunds(e, e.msg.sender);
	
	// execute some method
   	calldataarg arg; // any argument
	sinvoke f(e, arg); // simulate only non reverting paths 
	
	assert ( getTotalFunds(e) >= getFunds(e, e.msg.sender), "Total funds is less than a user funds " );
}

