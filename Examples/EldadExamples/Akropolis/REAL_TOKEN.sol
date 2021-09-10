  
import "./ERC20.sol";

contract MyToken is ERC20 {
    
    function deposit() public payable {
        // MINT IS HERE
        uint minted_tokens = msg.value;
        balances[msg.sender] += minted_tokens;
        total += minted_tokens;
    }
    
    function withdraw() public {
        // BURN IS HERE
        uint tmp_balance = balances[msg.sender];
        balances[msg.sender] = 0;
        total -= tmp_balance;
        msg.sender.call{value: tmp_balance}("");
    }
    
    function getAddress() public view returns(address) {
        return address(this);
    }
}