/**
			Specification file for Certora Prover 


		To run:

		certoraRun Bank.sol:Bank --verify Bank:IntegrityOfDeposit.spec

		Simple rule that check that integirty of deposit 

**/


rule integrityOfDeposit(uint256 amount, uint256 fundsBefore, uint256 fundsAfter) {
	/* The env type represents the EVM parameters passed in every 
	   call (msg.*, tx.*, block.* variables in solidity 
	 */
	env e; 
	// The environment is passed as the first argument*/
	// Save the funds before 
	require fundsBefore == getFunds(e, e.msg.sender);
	
	deposit(e, amount);
	
	require fundsAfter == getFunds(e, e.msg.sender);
	
	// Verify that the funds of msg.sender is the sum of the funds before and the amount passed  
	assert ( fundsBefore + amount == fundsAfter, "Deposit did not increase the funds as expected" );
}


rule callTraceProblem( ) {
	/* The env type represents the EVM parameters passed in every 
	   call (msg.*, tx.*, block.* variables in solidity 
	 */
	env e; 
	// The environment is passed as the first argument*/
	// Save the funds before 
	uint256 fundsBefore = getFunds(e, e.msg.sender);
	uint256 amount;
	deposit(e, amount);
	
	uint256 fundsAfter = getFunds(e, e.msg.sender);
	
	// Verify that the funds of msg.sender is the sum of the funds before and the amount passed  
	assert ( fundsBefore + amount == fundsAfter, "Deposit did not increase the funds as expected" );
}

