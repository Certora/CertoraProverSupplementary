/**
			Specification file for Certora Prover 


		First run only the rule totalFundsAfterDeposit:
		certoraRun BankFixed.sol:Bank --verify Bank:Additional.spec --settings -rule=totalFundsAfterDeposit

		This rule shows that in case that in the initial state the totalFunds was smaller than the user funds then there is a violation

		By adding a precondition we can verify this rule.
		run:

		certoraRun BankFixed.sol:Bank --verify Bank:Additional.spec --settings -rule=totalFundsAfterDepositWithPrecondition

**/


rule totalFundsAfterDeposit(uint256 amount, uint256 userFundsAfter, uint256 totalAfter ) {
	env e; 
	
	
	deposit(e, amount);
	
	require userFundsAfter == getFunds(e, e.msg.sender);
	require totalAfter == getTotalFunds(e);
	
	// Verify that the total funds of the system is at least as the current funds of the msg.sender
	assert ( totalAfter >=  userFundsAfter, "Total funds is less than a user funds " );
}



rule totalFundsAfterDepositWithPrecondition(uint256 amount, uint256 userFundsAfter, uint256 totalAfter ) {
	env e; 
	
	// Assume that in the current state before calling deposit, the total funds is at least as the user funds
	require  getTotalFunds(e) >= getFunds(e, e.msg.sender);
	deposit(e, amount);
	
	require userFundsAfter == getFunds(e, e.msg.sender);
	require totalAfter == getTotalFunds(e);
	
	// Verify that the total funds of the system is at least as the current funds of the msg.sender
	assert ( totalAfter >=  userFundsAfter, "Total funds is less than a user funds " );
}

