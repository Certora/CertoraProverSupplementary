In this tutorial, you will practice understanding counter-examples produced by Certora Prover. 
As we discussed, the tool assumes all possible input values and states as a starting state. Some of them are infeasible, which means that there is no set of operations starting from the constructor that will lead to that state. 

# Simple Example
Start with [Ball Game](BallGame/BallGame.sol), implementing a ball game with four players. Player 1 passes the ball to Player 2; Player 2 passes back to Player 1. Player 3 and 4 passes to each other. The ball starts at Player 1. Let's prove that the ball can never reach player 4.

* Run:  
  ```sh
  certoraRun BallGame.sol --verify BallGame:BallGame.spec 
  ```
* Understand the counter-example
* Fix the rule to avoid superfluous initial states

We learn here that in order to prove the required property we needed to prove a stronger invariant.

# Advanced Example 
Now, for a bit more realistic example, [Manager](Manager/Manager.sol) implements transferring management role of a fund. It is a requirement that an address can manage only one fund. Let's try to prove this property.

[Manager.spec](Manager/Manager.spec) contains a typical parametric rule 

* Run:  
  ```sh
  certoraRun Manager.sol --verify Manager:Manager.spec 
  ```
* Understand the counter-examples 
* Understand which additional properties are related and need to be proven together
* Fix the rule
* Check your rule as sometimes the rule is too strict, it limits the possible initial states or executions too much:
  - Insert bugs to the code that you believe should be uncovered and rerun Certora Prover 
  - Run on [ManagerBug1](Manager/ManagerBug1.sol) and [ManagerBug2](Manager/ManagerBug2.sol)
    
	To run on those files:
     ```sh
    certoraRun ManagerBug1.sol:Manager --verify Manager:Manager.spec --msg "check for bug"
	certoraRun ManagerBug2.sol:Manager --verify Manager:Manager.spec --msg "check for bug"
    ```
	Did your rule find any violations?

