# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401

# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame  # noqa
from datetime import datetime  # noqa
from typing import Optional, Union  # noqa

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter, stoploss_from_absolute)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class BTCEMAStrategyOptimized(IStrategy):
    """
    This is a strategy template to get you started.
    More information in https://www.freqtrade.io/en/latest/strategy-customization/

    You can:
        :return: a Dataframe with all mandatory indicators for the strategies
    - Rename the class name (Do not forget to update class_name)
    - Add any methods you want to build your strategy
    - Add any lib you need to build your strategy

    You must keep:
    - the lib in the section "Do not remove these libs"
    - the methods: populate_indicators, populate_entry_trend, populate_exit_trend
    You should keep:
    - timeframe, minimal_roi, stoploss, trailing_*
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = '1d'

    # Can this strategy go short?
    can_short: bool = True

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 100
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.1
    use_custom_stoploss=True

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 50

    # Strategy parameters
    buy_ema_fast_length: int = 7
    buy_ema_slow_length: int = 57
    sell_ema_fast_length: int = 30
    sell_ema_slow_length: int = 32

    # Optional order type mapping.
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'entry': 'gtc',
        'exit': 'gtc'
    }
    
    @property
    def plot_config(self):
        return {
            'main_plot': {
                'buy_ema_fast': {'color': 'lime'},
                'buy_ema_slow': {'color': 'green'},
                'sell_ema_fast': {'color': 'pink'},
                'sell_ema_slow': {'color': 'red'},
            },
            'subplots': {
            }
        }

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """

        # EMA - Exponential Moving Average
        dataframe['buy_ema_fast'] = ta.EMA(dataframe, timeperiod=self.buy_ema_fast_length)
        dataframe['buy_ema_slow'] = ta.EMA(dataframe, timeperiod=self.buy_ema_slow_length)
        dataframe['sell_ema_fast'] = ta.EMA(dataframe, timeperiod=self.sell_ema_fast_length)
        dataframe['sell_ema_slow'] = ta.EMA(dataframe, timeperiod=self.sell_ema_slow_length)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with entry columns populated
        """
        # long
        dataframe.loc[
            (
                (dataframe['close'] > dataframe["buy_ema_fast"])
                & (dataframe["buy_ema_fast"] > dataframe["buy_ema_slow"])
            ),
            'enter_long'] = 1
        # short
        dataframe.loc[
            (
                (dataframe['close'] < dataframe["sell_ema_fast"])
                & (dataframe["sell_ema_fast"] < dataframe["sell_ema_slow"])
            ),
            'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with exit columns populated
        """
        return dataframe

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime, current_rate: float, current_profit: float, **kwargs) -> float:
        stoploss = self.stoploss
        
        if self.dp:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)

            last_candle = dataframe.iloc[-1].squeeze()

            if trade.is_short:
                stoploss = stoploss_from_absolute(last_candle["sell_ema_slow"], last_candle['close'], is_short=trade.is_short)
            else:
                stoploss = stoploss_from_absolute(last_candle["buy_ema_slow"], last_candle['close'], is_short=trade.is_short)

            return stoploss