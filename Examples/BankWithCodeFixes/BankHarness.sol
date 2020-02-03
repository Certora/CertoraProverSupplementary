
import "Bank.sol";
contract BankHarness is Bank {

	function init_state() public {  }
	
	function _ercBalance() public returns (uint256){
		address account = msg.sender;
		return account.balance;
	}
	
	
}