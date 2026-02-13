import yfinance as yf
import pandas as pd 
import numpy as np 
from statsmodels.tsa.stattools import coint, adfuller
from scipy import stats 
import matplotlib.pyplot as plt 
import seaborn as sns 
from datetime import datetime, timedelta

class PairsTradingStrategy:
    """
    Pairs trading strategy using cointegration-based mean reversion

    strategy logic:
    1. test for cointegration between two assets
    2. calculate the spread (residuals form cointegration regression)
    3. generate signals when spread deviates >2 standard deviations
    4. entry: go long underperformer, short outperformer
    5. exit: when spread reverts to mean or hits stop loss
    """
    def __init__(self, ticker1, ticker2, start_date, end_date):
        """
        Initialize pairs trading strategy

        parameters:
            ticker1 (str): first stock ticker
            ticker2 (str): second stock ticker
            start_date (str): start date 'YYYY-MM-DD'
            end_date (str): end date 'YYYY-MM-DD'
        """
        self.ticker1 = ticker1
        self.ticker2 = ticker2
        self.start_date = start_date
        self.end_date = end_date
        self.prices = None
        self.spread = None
        self.zscore = None
        self.hedge_ratio = None
        self.signals = None
        self.portfolio = None
    
    def fetch_data(self):
        """download historical price data"""
        print(f"fetching data for {self.ticker1} and {self.ticker2}...")

        data = yf.download(
            [self.ticker1, self.ticker2],
            start = self.start_date,
            end = self.end_date,
            auto_adjust = True,
            progress = False
        )

        self.prices = pd.DataFrame({
            self.ticker1: data['Close'][self.ticker1],
            self.ticker2: data['Close'][self.ticker2]
        }).dropna()

        print(f"downloaded {len(self.prices)} days of data")
        return self.prices
    
    def test_cointegration(self, significance_level = 0.05):
        """
        test for cointegration using engle-granger method

        returns:
        dict: contains p-value, test statistic, and cointegration result
        """
        score, pvalue, _ = coint(
            self.prices[self.ticker1],
            self.prices[self.ticker2]
        )

        is_cointegrated = pvalue < significance_level

        result = {
            'test_statistic': score,
            'p_value': pvalue,
            'is_cointegrated': is_cointegrated,
            'significance_level': significance_level
        }

        print(f"\nCointegration Test Results:")
        print(f"Test Statistics: {score:.4f}")
        print(f"P-value: {pvalue:.4f}")
        print(f"Cointegrated at {significance_level} level: {is_cointegrated}")

        return result
    
    def calculate_spread(self):
        """
        calculate the spread using linear regression
        spread = stock1 - hedge_ratio * stock2
        """
        from scipy import stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            self.prices[self.ticker2],
            self.prices[self.ticker1]
        )

        self.hedge_ratio = slope

        spread_values = self.prices[self.ticker1] - self.hedge_ratio * self.prices[self.ticker2]
        
        if isinstance(spread_values, pd.DataFrame):
            self.spread = spread_values.iloc[:, 0]
        else:
            self.spread = spread_values

        spread_mean = self.spread.rolling(window=20).mean()
        spread_std = self.spread.rolling(window=20).std()
        self.zscore = ((self.spread - spread_mean) / spread_std).squeeze()

        print(f"\nSpread Calculation:")
        print(f"Hedge Ratio (beta): {self.hedge_ratio:.4f}")
        print(f"R-squared: {r_value**2:.4f}")
        print(f"Mean Spread: {self.spread.mean():.4f}")
        print(f"Std Dev Spread: {self.spread.std():.4f}")

        return self.spread, self.zscore
    
    def generate_signals(self, entry_threshold = 2.0, exit_threshold = 0.5):
        """
        generate trading signals based on z-score thresholds

        parameters:
            entry_threshold (float): z-score threshold for entering position (default: 2.0)
            exit_threshold (flaot): z-score threshold for exiting position (default: 0.5)
        returns:
            DataFrame: trading signals (-1: short spread, 0: no position, 1: long spread)
        """
        self.signals = pd.DataFrame(index = self.prices.index)
        self.signals['zscore'] = self.zscore
        self.signals['position'] = 0

        self.signals.loc[self.signals['zscore'] > entry_threshold, 'position'] = -1
        self.signals.loc[self.signals['zscore'] < entry_threshold, 'position'] = 1
        
        self.signals.loc[abs(self.signals['zscore']) < exit_threshold, 'position'] = 0

        self.signals['position'] = self.signals['position'].replace(0, np.nan).ffill().fillna(0)
        
        self.signals['trades'] = self.signals['position'].diff().fillna(0).abs()

        num_trades = (self.signals['trades'] > 0).sum()
        print(f"\nSignal Generation:")
        print(f"Entry Threshold: ±{entry_threshold} std devs")
        print(f"Exit Threshold: ±{exit_threshold} std devs")
        print(f"Total Trades: {num_trades}")

        return self.signals
    
    def backtest(self, initial_capital = 100000, transaction_cost = 0.001):
        """
        backtest the pairs trading strategy

        parameters:
            initial_capital (float): starting capital in dollars
            transaction_cost (float): transaction cost as percentage (default: 0.1%)
        returns:
            DataFrame: portfolio performance metrics
        """
        self.portfolio = pd.DataFrame(index = self.prices.index)
        
        returns1 = self.prices[self.ticker1].pct_change()
        returns2 = self.prices[self.ticker2].pct_change()
        
        # Position = 1: Long spread (long stock1, short stock2)
        # Position = -1: Short spread (short stock1, long stock2)
        
        self.portfolio['stock1_position'] = self.signals['position']
        self.portfolio['stock2_position'] = -self.signals['position'] * self.hedge_ratio
        
        self.portfolio['stock1_return'] = self.portfolio['stock1_position'].shift(1) * returns1
        self.portfolio['stock2_return'] = self.portfolio['stock2_position'].shift(1) * returns2
        
        self.portfolio['strategy_return'] = (
            self.portfolio['stock1_return'] + self.portfolio['stock2_return']
        )
        
        trades = self.signals['trades']
        transaction_costs = trades * transaction_cost
        self.portfolio['strategy_return'] = self.portfolio['strategy_return'] - transaction_costs
        
        self.portfolio['cumulative_return'] = (1 + self.portfolio['strategy_return']).cumprod()
        
        self.portfolio['portfolio_value'] = initial_capital * self.portfolio['cumulative_return']
        
        benchmark_return = (returns1 + returns2) / 2
        self.portfolio['benchmark_cumulative'] = (1 + benchmark_return).cumprod()
        self.portfolio['benchmark_value'] = initial_capital * self.portfolio['benchmark_cumulative']
        
        return self.portfolio

    def calculate_performance_metrics(self):
        """
        calculate performance metrics for the strategy

        returns:
            dict: performance metrics 
        """
        if self.portfolio is None:
            raise ValueError("Must run backtest() first")
        
        strategy_return = self.portfolio['strategy_return'].dropna()
        total_days = len(strategy_return)
        years = total_days / 252
        
        total_return = self.portfolio['cumulative_return'].iloc[-1] - 1
        annualized_return = (1 + total_return) ** (1/years) - 1
        volatility = strategy_return.std() * np.sqrt(252)
        sharpe_ratio = annualized_return / volatility if volatility > 0 else 0

        cumulative = self.portfolio['cumulative_return']
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        winning_days = (strategy_return > 0).sum()
        total_trading_days = (strategy_return != 0).sum()
        win_rate = winning_days / total_trading_days if total_trading_days > 0 else 0
        
        benchmark_return = self.portfolio['benchmark_cumulative'].iloc[-1] - 1
        outperformance = total_return - benchmark_return
        
        metrics = {
            'Total Return': f"{total_return*100:.2f}%",
            'Annualized Return': f"{annualized_return*100:.2f}%",
            'Volatility': f"{volatility*100:.2f}%",
            'Sharpe Ratio': f"{sharpe_ratio:.3f}",
            'Max Drawdown': f"{max_drawdown*100:.2f}%",
            'Win Rate': f"{win_rate*100:.2f}%",
            'Total Trades': int((self.signals['trades'] > 0).sum()),
            'Benchmark Return': f"{benchmark_return*100:.2f}%",
            'Outperformance': f"{outperformance*100:.2f}%"
        }

        print("\n" + "=" * 60)
        print("STRATEGY PERFORMANCE METRICS")
        print("=" * 60)
        for key, value in metrics.items():
            print(f"{key:.30} {value}")

        return metrics
