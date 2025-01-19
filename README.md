<h1 align="center"> SOLANA SNIPER BOT </h1> <br>
<p align="center">
  <a href=""> 
  </a>  
</p>

## Table of Contents

- [Features](#features)
- [Usage](#Usage)
- [Setting](#Setting-)
- [Disclaimer ](#Disclaimer)
- [Contact ](#Contact)


## Features

A few of the things you can do:

- Sniping: Execute buy transactions instantly when liquidity is added to a SPL token, ensuring you're among the first to buy in promising new tokens.
- Take Profit: Automatically sell tokens at a predefined profit percentage, securing gains.
- Buy/Sell x Times: Execute repeated buy orders to average down or scale into positions.
- Sell Limit Order: Set your tokens to sell automatically at a predetermined price, locking in profits.
- User friendly interface - hands-on interface
- **Making the first to trade in new tokens.**
<img width="910" alt="2" src="https://github.com/user-attachments/assets/a85bd1f2-c152-42a3-8b27-c3bb31cb59e2">


## Installation

- Download Python ( Recommend the latest version )  [Python 3.13.0](https://www.python.org/downloads/)
-  ***VERY IMPORTANT***: When installing Python also install **"Add python.exe to path"** and ***"Use admin privileges when installing py.exe:*** => Tick

## Usage


![GIF](https://github.com/Xianpwr/gif/raw/main/as.gif)

- Update `pip` Run the following command to update pip to the latest version

```python
python -m pip install --upgrade pip
```
- Clone or download the project

```git 
git clone https://github.com/Xianpwr/SOLANA_SNIPER_BOT.git
```

Option 2: Download the project directly

Go to the project's GitHub page, click the "Code" button and select "Download ZIP". Unzip the downloaded ZIP file to get the project folder.

- Navigate to the project folder

Open a terminal and navigate to the project folder

```python
cd SOLANA_SNIPER_BOT
```

- Install libraries

Run the following command to install the required libraries for the project:

```python
pip install -r requirements.txt
```

- Run the project

Run the following command to start the project:



```python
python main.py
```


## Setting
- **BALANCE** : Show Balance & Profit
- **BUY DELAY** : In seconds after launch. Set to 0, Token will buy immediately after token launch
- **TAKE PROFIT** : Take-Profit Order (TP) . Token places a sell order and confirms immediately after reaching the target
- **SELL DELAY** : to the number of seconds you want to wait before selling the token. Set to 0, token will be sold immediately after it is bought.
- **CHECK RUG** : Set to true to check the risk score and protect against rug pulls.



Example: 

<img width="1176" alt="s" src="https://github.com/user-attachments/assets/97d97112-703d-48f8-8075-a2de60d85cb1">


![image](https://github.com/user-attachments/assets/8b825c7d-1f6e-4178-a68c-af6c4dc4877d)




## Disclaimer

- This extension is not affiliated with Solana Foundation or Solana Labs. It is a non-profit community project.
- Solana Snipe is in active development, so all the snippets are subject to change.
- The snippets are unaudited. Use at your own risk.



# FOR SALE:
Multi chain and multi wallet sniper that works on a variety of decentralized exchanges as well. Optimized methods are used in order to make this one of the fastest, if not the fastest sniper on the market

## Interested in buying?
Sales have reopened. Message me on telegram if you are interested
- [Telegram](https://t.me/nonlinearlogic)


### Supported chains and exchanges
- Ethereum
    - Uniswap
    - Sushiswap

- Binance smart chain
    - Pancakeswap
    - Sushiswap
    - Apeswap
    - Backeryswap

- Polygon Matic
    - Quickswap
    - Apeswap
    - Defyn

- Kucoin Community Chain
    - Kuswap
    - KoffeSwap

- Okex Chain
    - CherrySwap

- Avalanche Mainnet C-Chain
    - Pangolin
    - Trader Joe

- Fantom Opera
    - Spirit Swap
    - Spooky Swap
    - Protofi

- Cronos Mainnet beta
    - Meerkat
    - VVS Finance
    - Cronaswap

- Harmony chain shard 0
    - Viper

- Metis Andromeda Mainnet
    - Netswap
    - Tethys


### Innovative UI
The bot has a UI which runs in the terminal, this allows you to run the bot on remote servers without needing a display server or having to play with virtual displays as you would with normal UIs.

![Loading screen](https://i.imgur.com/Rave54x.png)
![Working screen](https://i.imgur.com/Kl8FY6u.png)

### Current features
- Multi wallet support
- Support for custom pairs (Tokens that are paired to a different coin than the default one of the exchange)
- Instant buy functionality, you can make the bot Instantly skipping it's normal flow in case something changes after you've started it.
- Automatically detect owner, max buy, trading open functions and sell triggering functions (ex. mint, blacklist and so on)
- Mempool scan for liquidity scanning & trading open scanning
- Option to send multiple buy transactions at the same time (99% all get in the same block at relatively near positions from each other, depends also on the node you use)
- Honeypot prevention, you can set the bot to check if the token is a honeypot before buying.
- Max buy tax and max sell tax prevention, the bot will only sell if the current tax is below the amount you set.
- Anti-bot prevention, options to skip blocks/seconds after liquidity detection, option to skip blocks/seconds after trading enable detection, minimum liquidity check (to be added in v1.0.1) 
- Anti rug

### Changelogs

#### Version 1.0.0
- Initial release
- Added TUI (Text user interface), it's like GUI but you can run your bot in the terminal)
- Added support for multiple wallets
- Added automatic trading enable function detection
- Added automatic bad functions (sell triggering) detection
- Added automatic owner address detection
- Improved mempool speed and overall performance
- Improved sending transactions speed
- Option to change secondary wallets on your own

#### Version 1.0.1
- Fix small bugs from version 1.0.0
- Add option to set gas price and gas limit also from UI rather than config only
- Add netswap and Tethys on Metis chain

#### Version 1.0.2
- Support for ethereum chain and it's new gas system
- Support for buying exact amount of tokens
- Add missing chains and exchanges
- Fix bugs from version 1.0.1

#### Version 1.0.3
- Add rug pull prevention (sell when liquidity is about to be removed or when a bad function is about to be called on the token contract)
- Add option to scroll the token functions table at startup screen
- Add IPC node connection support
- Added anti rug system
- Improvements to mempool scan

#### version 1.1.0
- Implement minimum liquidity option
- Add everything related to selling the tokens, sell certain % of tokens, certain amounts of tokens. Sell based on take profit and stop loss


#### version 1.2.0
- Telegram scrapper added (features in telegram)


#### version 1.3.0
- Contract buy mode added (anti blacklist)
- You will have to deploy a contract on each corresponding chain!

#### version 1.3.1 
- Refactoring/performance improvements
