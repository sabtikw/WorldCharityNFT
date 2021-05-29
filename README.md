# NFT + Liquid Staking



## NFT
- All NFT purchases, deposit ETH to Liquid Staking protocol and recieve ERC20's for staked ETH (i.e Lido Finance)
- staked ETH added to a shared pool
- Creators recieve 5% of each purchased NFT
-  Rewards generated from staked ETH ( deposited ETH withdrawal is locked, only rewards are allowed to be withdrawn)
- 5% is taken off each transfer of the NFTs, stacked and  put into a the shared pool
- DAO decides what to do with the rewards i.e put it into a charity, distribute it to NFT owners, etc...



## This project uses :
-   OpenZeppelin ERC20, SafeMAth, ERC721, , Access Control, ReentrencyGuard
-   Brownie-eth (Python-based Developement Environment for Smart Contracts)
-   pytest unit testing
-   React, npm and etherjs



## TODO (this code is not complete)
1. Smart Contract :
   1. owner should have the ability to set amount for transfer when approve the NFT (see React/Transfer)
   2. use unstructured storage proxy pattern
   3. implement voting smart contract for the DAO or just use Aragon(see React/Gover) !
   4. remove some functions
2. Brownie-eth
   1. addd tests for events
   2. ensure 100% test coverage
3. React/Frontend
   1. Dashboard
      1. add world map with NFT ownership
   2. Govern
      1. implement Voting interface
   3. Transfer
      1. implement transfer interface
      2. approve transfer
      3. pay and claim
  