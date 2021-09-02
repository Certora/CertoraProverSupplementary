pragma solidity ^0.8.4;
import "./ERC20.sol";

contract Pool is ERC20 {
    address token0;
    address token1;
    address owner;

    uint token0Amount;
    uint token1Amount;
    uint K;

    
    constructor(address _token0, address _token1) {
        token0 = _token0;
        token1 = _token1;
        owner = msg.sender;
    }    
    
    function init_pool() public {
        require(msg.sender == owner);
        token0Amount = iERC20(token0).balanceOf(address(this));
        token1Amount = iERC20(token1).balanceOf(address(this));
        
        K = token0Amount * token1Amount; 
        balances[owner] = 100000;
        total = balances[owner];
    }

    function add_liquidity() public returns (uint) {
        // calculate added token0, token1 amounts
        uint added0 = iERC20(token0).balanceOf(address(this)) - token0Amount;
        uint added1 = iERC20(token1).balanceOf(address(this)) - token1Amount;

        // deposit to LP token
        uint units = mint(msg.sender, added0, added1);
        uint LP_total_supply = total;
        K = (K / (LP_total_supply-units)) * (LP_total_supply);
        
        sync();
        return units;
    }

    function remove_liquidity(uint LP_tokens) public {
        // sync();      // add sync() here to solve the bug
        burn(msg.sender, LP_tokens);
        uint LP_total_supply = total;
        K = K * LP_total_supply / (LP_total_supply + LP_tokens);
    }
    
    function swap(address from_token) public {
        // AMM
        require((from_token == token0 || from_token == token1), "Must be toekn0 or token1");
        address to_token = from_token == token0 ?  token1 : token0;
        uint from_token_balance = iERC20(from_token).balanceOf(msg.sender);
        iERC20(from_token).transferFrom(msg.sender, address(this), from_token_balance); // from customer to pool
        uint to_token_send = iERC20(from_token).balanceOf(msg.sender) * iERC20(to_token).balanceOf(msg.sender) - K;
        iERC20(to_token).transfer(msg.sender, to_token_send); // From the pool to the customer
        sync();
        
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