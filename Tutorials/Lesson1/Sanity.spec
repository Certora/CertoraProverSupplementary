/**
		Specification file for Certora Prover 


		First run only the rule totalFundsAfterDeposit:
		certoraRun BankFixed.sol:Bank --verify Bank:Additional.spec --settings -rule=totalFundsAfterDeposit

		This rule shows that when the initial state the totalFunds was smaller than the user funds, there is a violation. 

		By adding a precondition we can verify this rule.
		run:

		certoraRun BankFixed.sol:Bank --verify Bank:Additional.spec --settings -rule=totalFundsAfterDepositWithPrecondition

**/


rule totalFundsAfterDeposit(uint256 amount) {
	env e; 
	
	
	deposit(e, amount);
	
	uint256 userFundsAfter = getFunds(e, e.msg.sender);
	uint256 totalAfter = getTotalFunds(e);
	
	// Verify that the total funds of the system is at least the current funds of the msg.sender.
	assert ( totalAfter >=  userFundsAfter, "Total funds are less than a user's funds " );
}



rule totalFundsAfterDepositWithPrecondition(uint256 amount) {
	env e; 
	
	// Assume that in the current state before calling deposit, the total funds of the system is at least the user funds.
	require  getTotalFunds(e) >= getFunds(e, e.msg.sender);
	deposit(e, amount);
	
	uint256 userFundsAfter = getFunds(e, e.msg.sender);
	uint256 totalAfter = getTotalFunds(e);
	
	// Verify that the total funds of the system is at least the current funds of the msg.sender.
	assert ( totalAfter >=  userFundsAfter, "Total funds are less than a user's funds " );
}

