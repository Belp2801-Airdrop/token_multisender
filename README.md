## Description
<h3 align="center"> Token multisender</h3>
<p align="center">
  <picture align="center">
    <img src="https://github.com/user-attachments/assets/37aa6e2a-70ed-46ce-b431-13136047592b"</img>
  </picture>
</p>

Tool have 3 modes:

+ ***All***: transfer all token in wallet
+ ***Amount***: transfer a specific amount of token in wallet (same for all wallets)
+ ***Custom***: transfer a specific amount of token in wallet (custom for each wallet in .csv file)

Tool have 3 types:

+ ***Type 1: 1 to n***: transfer token from 1 wallet to many wallets
+ ***Type 2: n to 1***: transfer token from many wallets to 1 wallets
+ ***Type 3: n to n***: transfer token n wallets to n wallets (map 1-1)
  

## Installation
### Prerequisites
- Python 3 
### Setup
- Install libs
```
pip install -r requirements.txt
```

## Important Note

**Please test on testnet (Sepolia) before using this tool with mainnet (ETH. Base, Polygon,...)**

