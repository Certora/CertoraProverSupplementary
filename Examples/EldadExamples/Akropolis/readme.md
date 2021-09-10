## How to execute the attack:

0. start with user1
1. deploy AkropolisProtocol
2. deploy MyToken - the real token
3. deploy FAKE - the fake token
4. deposit 10 ether to MyToken
5. deposit to Arkopolis instance, parameters: <user1 address>, <real token address>, <real token address>, 1000000000000000000, 0
6. change user to user2
7. deposit 5 ether to MyToken
8. deposit to Arkopolis instance, parameters: <user2 address>, <fake token address>, <real token address>, 0, 0
9. withdraw the arkopolis balance.
10. withdraw from the real token.