# Certora Prover - Lesson 2 


In the previous lesson we have learned that as default, Certora prover ignores all paths where a function call reverts
However, reasoning about reverting path and fully understanding the precondition of a function can uncover bugs. 

By using the Certora Prover, one can formally prove all the cases of a reverting path.





## Reverting Paths

Let's look at the example of Bank.sol. We assume for start the getFunds function should not revert.


Rule [nonRevertBalanceOf](revert.spec#L14) calls [`getFunds`](Bank.sol) and reason also on reverting path by using the `@withrevert` annotation

> `getFunds@withrevert(e, account)`  

Next, the builtin Boolean variable `lastReverted` which is true when the last function call reverted is used.

So, This rule actually checks that all paths do not revert.
Running this rule
```sh
certoraRun Bank.sol:Bank --verify Bank:IntegrityOfDeposit.spec --settings -rule=nonRevertBalanceOf
```
results in a violation for the case that the account is inactive. 

Now, we can change the rule and make sure that this is the only condition for a revert.

```sh
certoraRun Bank.sol:Bank --verify Bank:IntegrityOfDeposit.spec --settings -rule=revertCharacteristic
```


However, when adding an assumptions, one should if this is a safe precondition. 
Could an account be inactive but still have funds?  

## Invariant

Let's define a  property of the bank state that should always hold:


`
funds[account] > 0 <==> active[account]    
`


This expression is an *invariant* -  a condition that should always holds, on all reachable state of the contract. 

Certora Prover verifies invariants similar to mathematical induction. First, the invariant is checked on the initial state of the contract.  
Next, each method is checked by assuming that the invariant holds before, calling the method, and verifying that the invariant holds on the resulting state.  


## Harness

*** continue here ***

Let's run the invariant 

Syntax:

invariant invariantName(args_list) exp - 

Assume exp holds before execution of any method and verify exp must hold afterwards. 
The invariant above is equivalent to a rule:
	method f;
	require exp;
	calldataarg arg; 
	sinvoke f(e,arg);
	assert exp;




