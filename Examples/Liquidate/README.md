# Example of a critical bug in liquidation
 
 A simplified version of a bug based on a real issue found in which the system losses assets. 

 A malicious user can call batchCalls with `actions[0] > 2` ,
 `callee[0] = address(BorrowSystem)`, and `datas[0]` arguments for liquidate.

 The `callee[i].call(datas[i])` would call liquidate, but the `msg.sender` would
 become BorrowSystem since liquidate is called by batchCalls, and it would
 result in loss of assets for the system. 
 
 The call to liquidate would result
 in BorrowSystem transferring borrowTokens to itself (no gain) and sending
 the collateralTokens outside the system (loss).
 
