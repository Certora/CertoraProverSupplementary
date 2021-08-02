/**
		Specification file for Certora Prover 


		To run:

		certoraRun Bank.sol:Bank --verify Bank:IntegrityOfDeposit.spec

		A simple rule that checks the integrity of the deposit function. 

		Understand the counter example and then rerun:

		certoraRun BankFixed.sol:Bank --verify Bank:IntegrityOfDeposit.spec 

**/

rule integrityOfDeposit(uint256 amount) {
	// The env type represents the EVM parameters passed in every 
	//   call (msg.*, tx.*, block.* variables in solidity).
	env e; 
	
	// Save the funds before a deposit.
	// The environment is passed as the first argument.
	uint256 fundsBefore = getFunds(e, e.msg.sender);
	
	deposit(e, amount);
	
	uint256 fundsAfter = getFunds(e, e.msg.sender);
	
	// Verify that the funds of msg.sender is the sum of her funds before and the amount deposited.  
	assert ( fundsBefore + amount == fundsAfter, "Deposit did not increase the funds as expected" );
}

