# CandleGenie-Prediction-Bot
Bot that automates bets on Candle Genie Predictions using technicals from trading view.

<br /><br />
Features:
- Scrapes technical analysis summary data from Trading view and uses this to place bets.
- Current setup for BNB and BTC prediction (can easily be modified to work with Eth predictions).
- Automates collection of wins and refunds when balance becomes low (for the lowest possilbe claim fees).
- Outputs wallet balance to personal telegram.
- ~66% win rate under certain market conditions.
<br /><br />


How to use:
- Install telegram-send: https://pypi.org/project/telegram-send/#installation
- Change ADDRESS and PRIVATE_KEY variable to the address and private key of your wallet inside config.py.
- Change ADDRESS variable to you wallet address inside wallet.py.
- Run main.py. 
