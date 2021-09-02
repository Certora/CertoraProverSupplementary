
/* 
    Assume - all tokens worths 1$, including AkropolisProtocol token.
*/

contract AkropolisProtocol {
    uint total = 0;
    mapping (address => uint) balances;

    function deposit(address[] memory tokens, uint[] memory amounts) public {
        uint beforeFunds = calcTotalFunds(tokens);
        transferToProtocol(tokens, amounts);
        uint afterFunds = calcTotalFunds(tokens);
        uint nDeposit = afterFunds - beforeFunds;
        balances[msg.sender] += nDeposit;
        total += nDeposit;
    }

    function transferToProtocol(address[] memory tokens, uint[] memory amounts) public {
        for (uint i=0; i<tokens.length; i++) {
            iERC20(tokens[i]).transferFrom(msg.sender, address(this), amounts[i]);
        }
    }

    function calcTotalFunds(address[] memory tokens) private returns (uint) {
        uint ret = 0;
        for (uint i=0; i<tokens.length; i++) {
            ret += iERC20(tokens[i]).balanceOf(address(this)); // * token rate - assume all tokens with the same worth
        }
        return ret;
    }

    function withdraw(address[] memory tokens, uint[] memory amounts) public {
        for (uint i=0; i<tokens.length; i++) {
            require(balances[msg.sender] >= amounts[i]);
            balances[msg.sender] -= amounts[i];
            iERC20(tokens[i]).tranfer(msg.sender, amounts[i]);
        }
    }
}