# Certora Prover Supplementary Material
Given the [Borda count election algorithm](https://en.wikipedia.org/wiki/Borda_count), 
a simple election scheme where voters rank candidates in order of preference by giving 3 points to their first choice, 
2 for their 2nd choice and 1 point for the 3rd choice. 

We define `BordaInterface` a general interface for the Borda algorithm: 
   * `winner() : address`  
   Returns the current winner
   * `points(address c) : uint256`  
    number of points candidate c has
   * `voted(address x): bool`  
    has user x voted?  
   * `vote(address f, address s, address t)`  
    msg.sender votes with first choice to f, second to s and third to t

[Borda.sol](Borda.sol) contains `BordaInterface` and a contract `Borda` implementing this interface.
[Borda.spec](Borda.spec) contains rules to verify any given implementation this interface.
   
To command to run the Certora Prover on contract Borda is:
```sh
certoraRun Borda.sol --verify Borda:Borda.spec
```

The challenge here is to introduce a bug or malicious code to the solidity code that is not detected by the rules. 
Note that you can not change the interface but beside that fell free to change the implementation 
add even add additional methods. 

Once you find a bug that is not detected by the spec, define the property that will uncover this issue. 

 