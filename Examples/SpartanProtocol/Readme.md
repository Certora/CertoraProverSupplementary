How to perform the attack:

1. Deploy 2 instances of MyToken - token0, token1.
2. Deploy SpartanPool where token0 and token1 are the cotracts addresses deployed at step 1.
3. Deposit 10 ether to token0 and another 10 ether to token1.
4. Transfer the 10 ether to the pool in both token0 and token1 (token0.transfer(pool_address, 1000000000), token1.transfer(pool_address, 1000000000)).
5. Press init_pool() at the pool contract.
6. Switch user. [to user2]
7. Deposit 16 ether to token0 and another 16 ether to token1.
8. Transfer the 8 ether to the pool in both token0 and token1.
9. Press add_liquidity() at the pool contract.
10. Transfer the left 8 ether to the pool in both token0 and token1.
11. Press remove_liquidity(80000) at the pool contract.
12. Press add_liquidity() at the pool contract.
13. Press remove_liquidity(124137) at the pool contract.
14. Press withdraw() at token0 and token1 contracts.

Steps 1-5 are used to build the pool. The actual attack happens at 6-14 and the attacker is user2 (the user we switched to) which ends with 7 ether more than had at step 6.