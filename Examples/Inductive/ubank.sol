contract                    bank { 
    
    mapping (address => uint256) public balances; 
    uint256 total;


  function deposit(address a, uint256 amount) public {   
     require(total + amount >= amount);
     //  forall address a. balances[a] <= total
     balances[a] += amount;// no overflow
     total += amount;
  }

  function withdraw(address b, uint256 amount)  public {          
    require(balances[b] >= amount);    
    balances[b] -= amount;  
    total -= amount;  
}
  function transfer(address from, address to, uint256 amount) public {
    require(balances[from] >= amount); 
     uint256 newFrom = balances[from]-amount;
     uint256 newTo = balances[to]+amount;
     balances[from] = newFrom;  
     balances[to] = newTo;
}

 function corretTransfer(address from, address to, uint256 amount) public {
    require(balances[from] >= amount); 
     require(from != to);
     uint256 newFrom = balances[from]-amount;
     uint256 newTo = balances[to]+amount;
     balances[from] = newFrom;  
     balances[to] = newTo;
}

   function getTotal() public returns (uint256)  {
     return total;
   }
  
}