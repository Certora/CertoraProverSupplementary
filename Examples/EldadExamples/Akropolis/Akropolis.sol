/* 
    Assume - all tokens worths 1$, including AkropolisProtocol token.
*/
import "ERC20.sol";

contract AkropolisProtocol {
    uint total = 0;
    mapping (address => uint) balances;
    
    event Deposit(uint TheAmount);

    function deposit(address user, address token0, address token1, uint amount0, uint amount1) public {
        uint beforeFunds = calcTotalFunds(token0, token1);
        transferToProtocol(user, token0, token1, amount0, amount1);
        uint afterFunds = calcTotalFunds(token0, token1);
        uint nDeposit = afterFunds - beforeFunds;
        balances[user] += nDeposit;
        total += nDeposit;
        emit Deposit(nDeposit);
    }

    function transferToProtocol(address user, address token0, address token1, uint amount0, uint amount1) private {
        iERC20(token0).transferFrom(user, address(this), amount0);
        iERC20(token1).transferFrom(user, address(this), amount1);
    }

    function calcTotalFunds(address token0, address token1) private returns (uint) {
        uint ret = 0;
        ret += iERC20(token0).balanceOf(address(this)); // * token rate - assume all tokens with the same worth
        ret += iERC20(token1).balanceOf(address(this));
        return ret;
    }

    function withdraw(address token, uint amount) public {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;
        iERC20(token).transferFrom(address(this), msg.sender, amount);
    }

    function getBalance() public returns(uint) {
        return balances[msg.sender];
    }
}