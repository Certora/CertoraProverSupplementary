contract bank { 
  enum Account {Alice,  Bob}
  mapping (Account => uint256) balances; 
  uint256 total;


  function deposit(Account a, uint256 amount) public {   
    require(total + amount >= amount);
    //  balances[Alice] <= total
    // balances[Bob] <= total
    balances[a] += amount;// no overflow
    total += amount;
  }

  function withdraw(Account b, uint256 amount)  public {          
    require(balances[b] >= amount);    
    balances[b] -= amount;  
    total -= amount;  
  }

  function transfer(Account from, Account to, uint256 amount) public { 
    require(balances[from] >= amount); 
    uint256 newFrom = balances[from]-amount;
    uint256 newTo = balances[to]+amount;
    balances[from] = newFrom;  
    balances[to] = newTo;
  }

  function getTotal() public returns (uint256)  {
    return total;
  }
  
  function getBalanceBob() public returns (uint256)  {
    return balances[Account.Bob];
  }
  function getBalanceAlice() public returns (uint256) {
    return balances[Account.Alice];
  }
}