# Freqtrade

This is my personal [Freqtrade](https://freqtrade.io) setup. Learn from it but don't use it blindly 😉

![Freqtrade](https://www.freqtrade.io/en/stable/images/logo.png)

## Strategies

+ [EmaStrategy](./user_data/strategies/EMAStrategy.py)

## Setup

```bash
# Setup the docker-compose.yml and .env files
make init

# Pull the image so we can use it
docker-compose pull

# Create a new config file
docker-compose run --rm freqtrade new-config --config ./user_data/config/freqtrade.json

# Start the containers
make up
make start # alias for `make up`
docker-compose up -d # do it manually

# Stop the containers
make down
make stop # alias for `make down`
docker-compose down --remove-orphans

# Restart the containers
make restart
docker-compose down --remove-orphans && docker-compose up -d
```

## Freqtrade Command

```
freqtrade --help
usage: freqtrade [-h] [-V]
                 {trade,create-userdir,new-config,new-strategy,download-data,convert-data,convert-trade-data,trades-to-ohlcv,list-data,backtesting,backtesting-show,backtesting-analysis,edge,hyperopt,hyperopt-list,hyperopt-show,list-exchanges,list-markets,list-pairs,list-strategies,list-timeframes,show-trades,test-pairlist,convert-db,install-ui,plot-dataframe,plot-profit,webserver}
                 ...

Free, open source crypto trading bot

positional arguments:
  {trade,create-userdir,new-config,new-strategy,download-data,convert-data,convert-trade-data,trades-to-ohlcv,list-data,backtesting,backtesting-show,backtesting-analysis,edge,hyperopt,hyperopt-list,hyperopt-show,list-exchanges,list-markets,list-pairs,list-strategies,list-timeframes,show-trades,test-pairlist,convert-db,install-ui,plot-dataframe,plot-profit,webserver}
    trade               Trade module.
    create-userdir      Create user-data directory.
    new-config          Create new config
    new-strategy        Create new strategy
    download-data       Download backtesting data.
    convert-data        Convert candle (OHLCV) data from one format to another.
    convert-trade-data  Convert trade data from one format to another.
    trades-to-ohlcv     Convert trade data to OHLCV data.
    list-data           List downloaded data.
    backtesting         Backtesting module.
    backtesting-show    Show past Backtest results
    backtesting-analysis
                        Backtest Analysis module.
    edge                Edge module.
    hyperopt            Hyperopt module.
    hyperopt-list       List Hyperopt results
    hyperopt-show       Show details of Hyperopt results
    list-exchanges      Print available exchanges.
    list-markets        Print markets on exchange.
    list-pairs          Print pairs on exchange.
    list-strategies     Print available strategies.
    list-timeframes     Print available timeframes for the exchange.
    show-trades         Show trades.
    test-pairlist       Test your pairlist configuration.
    convert-db          Migrate database to different system
    install-ui          Install FreqUI
    plot-dataframe      Plot candles with indicators.
    plot-profit         Generate plot showing profits.
    webserver           Webserver module.

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
```