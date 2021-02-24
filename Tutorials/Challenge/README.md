# Certora Prover Supplementary Material
The [Borda count election algorithm](https://en.wikipedia.org/wiki/Borda_count) is a simple election scheme where voters rank candidates in order of preference by giving 3 points to their first choice, 2 for their 2nd choice, and 1 point for the 3rd choice. 

We define `BordaInterface`, a public interface for the Borda algorithm: 
   * `winner(): address`  
   Returns the current winner - the address that has the most points. If there is more than one winner, one of them will be returned. If no votes were cast yet, it returns the zero address.
   * `points(address c): uint256`  
   Returns the number of points candidate c has received.
   * `voted(address x): bool`  
   Returns true if user x voted and false otherwise.  
   * `vote(address f, address s, address t)`  
   msg.sender votes with f as the first choice, s as the second, and t as the third. The three addresses must be different. msg.sender can vote to itself.

[Borda.sol](Borda.sol) contains `BordaInterface` and a contract `Borda` implementing this interface.
[Borda.spec](Borda.spec) contains rules to verify any given implementation this interface.
   
To command to run the Certora Prover on contract Borda is given in [run.sh]. Add the path to your local solidity compiler with `--solc path/to/solc`.

The challenge is to introduce a bug or a malicious code to the `Borda` contract that the automated Certora prover does not detect with the given specification file [Borda.spec]. Note that you can not change `BordaInterface`. Feel free to change `Borda` as you like and even add additional methods. 

Once you find a bug that the prover does not identify, define a property that will uncover this issue. 

 