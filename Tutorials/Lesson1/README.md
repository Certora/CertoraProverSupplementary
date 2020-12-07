# Certora Prover Lesson 1 


## Overview of the technology
The Certora Prover is based on well-studied techniques from the formal verification community. 
***Specifications*** define a set of rules that call into the contract under analysis and make various assertions about its behavior. 
Together with the contract under analysis, these rules are compiled to a logical formula called a ***verification condition***, which is then proved or disproved by an SMT solver. 
If the rule is disproved, the solver also provides a concrete test case demonstrating the violation.

The rules of the specification play a crucial role in the analysis. Without adequate rules, only very basic properties can be checked (e.g., no assertions in the contract itself are violated). 
To effectively Certora Prover, users must write rules that describe the high-level properties they wish to verify on their contracts. 
Here we will learn how to think about and write high-level properties.


## Example

Lets take as an example a straightforward simple bank implementation ([Bank.sol](Bank.sol)).
The contract has a mapping from users to their funds, and the total funds deposited in the system. The basic operations are `deposit` `transfer` and `withdraw`.

## A basic rule

Thinking about the function `deposit`, a basic property is:  
  
  #### _***P1 Correct deposit functionality***: The balance of the beneficiary is increased appropriately_  

The rule in [integrityOfDeposit.spec](IntegrityOfDeposit.spec) verifies this property. 
It verifies that the funds of `msg.sender` are his funds before plus the amount deposited.  
Formal verification can provide complete coverage of the input space, giving guarantees beyond what is possible from testing alone.
First, all possible inputs to the deposit function are taken into account.
All possible calling contexts (like msg.sender, timestamp, and block number) are represented in the `env` structure. 
The initial state can contain any value for the current funds of the msg sender.

To use the Certora Prover on this contract, run the following command line:

```sh
certoraRun Bank.sol:Bank --verify Bank:IntegrityOfDeposit.spec
```

This command is a basic verification of one contract, checking all rules in the specification file. 
Later on, we will see options to analyze a system containing many solidity files. 
Local solidity files are compiled, and the specification file is checked for syntax errors. 
Then they are compressed and sent to Certora’s web server.
The prover will print various information to the console. 
An email will be sent when the process is finished.
In the end, the output will look similar to this:
```
. . . 
Status page: https://vaas-stg.certora.com/jobStatus/23658/e145eb5d7d5f2dea1f72?anonymousKey=f49a8d71d3d17288d8405c015
Verification results: https://vaas-stg.certora.com/output/23658/e145eb5d7d5f2dea1f72/?anonymousKey=f49a8d71d3d17288d8405c0150
Prover found violations:
[rule] callTraceProblem
[rule] integrityOfDeposit
```
Follow the Verification results link to see the results.

Certora Prover helps in understanding violations of properties. 
You see a table with the verification results. ![results](images/results.jpg) 


For each rule, it either displays a thumbs-up when it is formally proved or a thumbs-down when it is violated.

Click the rule name to see a counter-example violating the rule.

![counter example](images/callTraceAndVariables.jpg) 

The counter-example shows values of the rule's parameters and variables and a call trace.
Drill down into the call trace to see which functions were called.
Notice the values of variables.  
The amount deposited in `deposit(e, amount);` is MAX_UNIT,   
the `uint256 fundsBefore = getFunds(e, e.msg.sender)` is 1 and   
the ` fundsAfter = getFunds(e, e.msg.sender)` is zero. 
So, what's the bug?  
**The rule does not hold when an overflow occurs.**


Let's "fix" the overflow bug in the code and rerun:
```sh 
certoraRun BankFixed.sol:Bank --verify Bank:IntegrityOfDeposit.spec
```


No violations were found. Great!   
Let’s define [another property](sanity.spec) and verify that after deposit, the totalFunds in the system is at least the funds of the msg.sender:  
  
 #### _***P2 Sanity of deposit***: total funds >= funds of a single user_
  


run:  
```sh
certoraRun BankFixed.sol:Bank --verify Bank:Additional.spec --settings -rule=totalFundsAfterDeposit
```

Notice the useful option of `-rule` to run one rule at a time.

A violation is found. 
Do you understand why?
Adding additional variables to the rule can help understand the counter-example. 

Try adding the ***helper variables*** `userFundsBefore` and `totalBefore`.
As we discussed, the tool assumes all possible input states as a starting state. 
The rule is violated when the initial state's totalFunds is less than the current funds of msg.sender. 
By adding ***preconditions***, you can eliminate infeasible states and put constraints on values. 
rule `totalFundsAfterDepositWithPrecondition` has the constraint 
`require  getTotalFunds(e) >= getFunds(e, e.msg.sender);`

The prover will now assume that in the initial state before calling deposit, the total funds are at least the user funds.
```sh
certoraRun BankFixed.sol:Bank --verify Bank:Additional.spec --msg “running with precondition”
```

Use the `--msg` flag to add a message description to your run. 
It can help you recognize a specific run.
You will see the message in the run results mail.


This property can be generalized to hold on all functions

 #### _***P3 Sanity of total funds: total funds >= funds of a single user_

To do so we introduce the notion of parametric rules.  
In order to simulate the execution of all functions in the main contract, 
you can define a method variable, `method f `, as a parameter to the rule or as a local variable.
Most common usage is as follows to simulate any function on any arguments
```
calldataarg arg; // any argument
sinvoke f(e, arg); //simulate only non reverting paths
```
Run the parametric rule from [parametric.spec](parametric.spec)
```sh
certoraRun Bank.sol:Bank --verify Bank:Parametric.spec
```
The rule is thumbs-up only if it was verified on all methods. 
For every function in the main contract, an inner rule is created, and shown in the lower table.
Click on the function name to see the counter example
See how many issues this rules detects. Are they all fixed?
```sh
 	certoraRun BankFixed.sol:Bank --verify Bank:Parametric.spec
```

The generalization of this rule to all functions have found another issue in transfer. 
One can transfer to himself to gain more assets. 

Parametric rules enable expressing reusable and concise correctness conditions. 
Note that they are not dependent on the specification, can be easily integrated into the CI to verify changes to the code including signature change, adding another function and  implementation changes. 














