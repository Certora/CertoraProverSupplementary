
                            contract                    bank { 
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