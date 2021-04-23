In this tutorial, you will practice understanding counter-examples produced by Certora Prover. 
As we discussed, the tool assumes all possible input values and states as a starting state. Some of them are infeasible, which means that there is no set of operations starting from the constructor that will lead to that state. 

Start with [Ball Game](Ball.sol), implementing a ball game with four players. Player 1 passes the ball to Player 2; Player 2 passes back to Player 1. Player 3 and 4 passes to each other. The ball starts at Player 1. Let's prove that the ball can never reach player 4.

run:  
```sh
certoraRun BallGame.sol --verify BallGame:BallGame.spec 
```

Understand the counter-example, fix the rule to avoid superfluous initial states. 
We learn here that in order to prove the required property we needed to prove a stronger property.


Now, for a bit more realistic example, [Manager](Manager.sol) implements transferring management role of a fund. It is a requirement that an address can manage only one fund. Let's try to prove this property.

[Manager.spec](Manager.spec) contains a typical parametric rule 

 run:  
```sh
certoraRun Manager.sol --verify Manager:Manager.spec 
```

Understand the counter-examples understand which additional properties are related and need to be proven together.

Sometimes, we have a rule that is too strict, it limits the possible initial states or executions too much. The best way to check a rule is to insert bugs to the code and make sure they are uncovered by the rules.
Insert bugs that you believe should be uncovered. Use also [ManagerBug1](ManagerBug1.sol) and [ManagerBug2](ManagerBug2.sol)
to run on those files:
```sh
certoraRun ManagerBug1.sol:Manager --verify Manager:Manager.spec --msg "check for bug"
```


