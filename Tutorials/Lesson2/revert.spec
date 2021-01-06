/**
		Specification file for Certora Prover 


		
		certoraRun Bank.sol:Bank --verify Bank:revert.spec 

		This spec file shows how to reason wbout reverting paths. 

		Reasoning about reverting path and understaing the preconditions can uncover bugs
**/


rule nonRevertBalanceOf(address account, bool isActive){
	env e;
	require isactive == isActive(e,account);
	getFunds@withrevert(e, account); 
	// lastReverted is a bollean builtin variable. It is true when the last function call reverted
    bool success = !lastReverted;
	assert(success, "getFunds should always succedd");
}

rule revertCharacteristic(address account, bool isActive) {
	env e;
	require isactive == isActive(e,account);
	getFunds@withrevert(e, account); 
	bool success = !lastReverted;
	assert( isactive => success, "getFunds should succedd on all active accounts");
}