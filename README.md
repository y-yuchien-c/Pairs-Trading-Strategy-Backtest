# Pairs Trading Strategy: Statistical Arbitrage with Mean Reversion

A quantitative trading strategy exploring mean-reversion opportunities in equity pairs through rigorous cointegration analysis. This implementation demonstrates both successful strategy mechanics **and the critical importance of statistical validation** - including when to reject a trading hypothesis.

## Executive Summary

**Trading Pair:** Coca-Cola (KO) vs. PepsiCo (PEP)  
**Strategy Type:** Market-neutral statistical arbitrage  
**Backtest Period:** January 2022 - January 2025 (3 years)

**Key Results:**
- **Total Return:** -0.19% (Strategy) vs. +5.48% (Benchmark)
- **Sharpe Ratio:** -0.005 (negative risk-adjusted returns)
- **Maximum Drawdown:** -15.57%
- **Win Rate:** 52.04% (39 trades)
- **Cointegration Test:** p-value = 0.81 (**FAILED** - pair not cointegrated)

**Critical Finding:** Despite strong business rationale and surface-level similarity, KO and PEP **lack the statistical cointegration required** for pairs trading during this period. The strategy underperformed by 5.67%, validating the importance of rigorous statistical testing over intuitive pair selection.

## Why This Project Matters

This analysis demonstrates a crucial principle in quantitative finance: **statistical validation must precede strategy deployment**, regardless of how compelling the narrative appears.

### What This Project Shows

**✓ Proper Methodology:**
- Implemented industry-standard cointegration testing (Engle-Granger)
- Rigorous backtesting with transaction costs (10 bps per trade)
- Market-neutral position construction with hedge ratio estimation
- Comprehensive performance analytics vs. benchmark

**✓ Intellectual Honesty:**
- Recognized when statistical evidence contradicts business intuition
- Documented why the strategy failed (no cointegration relationship)
- Demonstrated understanding of when to reject a trading hypothesis

**✓ Production Thinking:**
- Pre-trade validation catches unprofitable strategies before capital deployment
- Out-of-sample testing reveals regime changes (relationship broke down 2022-2025)
- Shows importance of continuous monitoring - pairs can decorrelate

**This is more valuable than a "perfect" backtest** - it shows you won't deploy capital on flawed premises.

## The KO/PEP Hypothesis: Why We Expected Cointegration

The pair selection wasn't arbitrary - there were solid fundamental reasons to expect a statistical relationship:

### Business Rationale
- **Market Structure**: Duopoly in carbonated soft drinks (~50% combined US market share)
- **Product Overlap**: Both compete in soda, juice, sports drinks, bottled water
- **Shared Drivers**: Consumer spending, commodity costs (sugar, aluminum, PET resin), retail distribution
- **Revenue Exposure**: Similar international diversification and brand-focused business models

### Why The Relationship Failed (2022-2025)

**Regime Change Hypothesis:**
1. **Divergent Strategic Pivots**:
   - PEP's snack food division (Frito-Lay) insulated it from beverage headwinds
   - KO remained pure-play beverage, more exposed to changing consumer preferences
   
2. **Different Inflation Exposure**:
   - PEP benefited from inelastic snack demand during inflation
   - KO faced elasticity in premium beverage pricing
   
3. **Post-COVID Consumption Patterns**:
   - Shift to at-home consumption favored PEP's grocery-focused distribution
   - KO's restaurant/fountain business recovered unevenly

**Statistical Evidence:**
- **R² = 0.164**: Only 16.4% of KO's variance explained by PEP (weak relationship)
- **Hedge Ratio β = 0.21**: Low beta suggests limited common movement
- **p-value = 0.81**: Cannot reject null hypothesis of no cointegration (threshold: 0.05)

**Key Insight:** Fundamental linkages don't guarantee statistical cointegration. Pairs can decorrelate during regime shifts, and pre-trade validation catches this.

## Methodology

### 1. Cointegration Testing (Engle-Granger Method)

**Two-Step Process:**
```
Step 1: Regress KO_t = α + β * PEP_t + ε_t  (estimate hedge ratio)
Step 2: Test if residuals ε_t are stationary (ADF test)
```

**Acceptance Criteria:**
- p-value < 0.05 → Reject null hypothesis → Residuals stationary → Pair cointegrated ✓
- p-value ≥ 0.05 → Cannot reject null → Residuals non-stationary → No cointegration ✗

**Our Results:**
- Test Statistic: -1.37
- **p-value: 0.81** (far above 0.05 threshold)
- **Conclusion: NOT COINTEGRATED** → Strategy invalid for this pair/period

### 2. Spread Construction & Signal Generation

Despite failed cointegration, we proceeded with backtest to quantify the cost of ignoring statistical warnings:

**Spread Calculation:**
```
Spread_t = KO_t - 0.2108 * PEP_t
```

**Z-Score Normalization:**
```
Z_t = (Spread_t - μ_20) / σ_20
```
Where μ and σ are 20-day rolling statistics.

**Trading Rules:**
- **Entry**: |Z-score| > 2.0 (spread >2 standard deviations from mean)
- **Exit**: |Z-score| < 0.5 (spread reverts toward mean)
- **Position**: Long spread when Z < -2.0, Short spread when Z > +2.0

### 3. Backtest Results: The Cost of Ignoring Statistics

| Metric | Pairs Strategy | Buy & Hold | Difference |
|--------|---------------|------------|------------|
| Total Return | **-0.19%** | **+5.48%** | **-5.67%** |
| Annualized Return | -0.06% | +1.79% | -1.85% |
| Volatility | 12.92% | ~14%* | Lower vol, but negative returns |
| Sharpe Ratio | **-0.005** | **~0.13** | Negative vs. positive |
| Max Drawdown | -15.57% | ~-12%* | Worse than benchmark |
| Win Rate | 52.04% | - | Barely above coin flip |
| Total Trades | 39 | - | Incurred 39 × 0.1% × 2 = 7.8% in costs |

*Benchmark estimates based on equal-weight KO/PEP portfolio

### Key Observations

1. **Transaction Costs Killed Returns**: 39 trades × 2 legs × 0.1% = 7.8% drag on performance
2. **No Mean Reversion Edge**: 52% win rate suggests no predictive power (random)
3. **Failed to Hedge Market Risk**: -15.57% drawdown shows positions weren't truly market-neutral
4. **Spread Didn't Revert**: Without cointegration, spread can trend indefinitely

**Bottom Line:** The cointegration test saved us from deploying this strategy. This validation framework works as intended.

## What We Learned: Regime Changes & Pair Selection

### Why Historical Cointegration Breaks Down

1. **Business Model Divergence**: Companies evolve - PEP's snack business created asymmetric exposure
2. **Macro Regime Shifts**: 2022-2025 saw inflation, supply chain shocks, consumption changes
3. **Lookback Period Matters**: Pair may have been cointegrated pre-2022 but decorrelated since

### Better Pair Selection Criteria

**Strong Cointegration Candidates:**
- **Same-sector, similar cap**: XOM/CVX (integrated oil), JPM/BAC (large cap banks)
- **Parent-subsidiary relationships**: Class A vs. Class B shares
- **ETF arbitrage**: SPY vs. basket of top 10 holdings
- **Geographic peers**: KO in US vs. international markets (currency-adjusted)

**Red Flags (like KO/PEP):**
- **Different business mix**: One company more diversified
- **Asymmetric exposures**: Different sensitivity to macro factors
- **Low R²**: Regression explains <50% of variance
- **High p-value**: Statistical test fails

## Future Enhancements

### Statistical Improvements
- [ ] **Rolling Cointegration Test**: Monitor relationship stability over time
- [ ] **Johansen Test**: Extend to portfolios (e.g., beverage basket vs. snack basket)
- [ ] **Half-Life Analysis**: Calculate expected mean-reversion time before entering trades
- [ ] **Out-of-Sample Validation**: Train on 2018-2021, test on 2022-2025

### Better Pair Discovery
- [ ] **Sector Screening**: Automated cointegration testing across S&P 500 pairs
- [ ] **Correlation Clustering**: Find groups of cointegrated stocks (statistical arbitrage baskets)
- [ ] **Fundamental Filters**: Pre-screen for business similarity before statistical tests

### Risk Management
- [ ] **Stop Loss**: Exit if spread diverges beyond historical max (regime detection)
- [ ] **Dynamic Thresholds**: Adjust entry/exit based on recent volatility
- [ ] **Position Limits**: Cap exposure per pair to manage tail risk

### Production Pipeline
- [ ] **Live Monitoring**: Real-time cointegration p-value tracking
- [ ] **Regime Detection**: HMM or structural break tests to pause trading
- [ ] **Multi-Pair Portfolio**: Combine 10+ uncorrelated pairs for stable returns

## Visualizations

1. **[Price Relationship](visualizations/price_relationship.html)**: Shows KO/PEP divergence over time
2. **[Spread & Signals](visualizations/spread_and_signals.html)**: Z-score volatility without mean reversion
3. **[Strategy Performance](visualizations/strategy_performance.html)**: Underperformance vs. benchmark
4. **[Monthly Returns](visualizations/monthly_returns.html)**: Inconsistent P&L distribution

## Installation & Usage
```bash
# Clone repository
git clone https://github.com/y-yuchien-c/pairs-trading-strategy-backtest.git
cd pairs-trading-backtest

# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run analysis
jupyter notebook notebooks/pairs_analysis.ipynb
```

### Test a Different Pair
```python
from src.pairs_trading import PairsTradingStrategy

# Try JPM/BAC (better candidates - same sector, similar cap)
strategy = PairsTradingStrategy(
    ticker1='JPM',
    ticker2='BAC',
    start_date='2022-01-01',
    end_date='2025-01-01'
)

strategy.fetch_data()
result = strategy.test_cointegration()

if result['is_cointegrated']:
    print("✓ Pair passed statistical validation")
    strategy.calculate_spread()
    strategy.generate_signals()
    strategy.backtest()
    strategy.calculate_performance_metrics()
else:
    print("✗ Pair failed - do NOT trade")
```

## Technical Implementation

**Libraries:**
- `statsmodels`: Engle-Granger cointegration test, ADF stationarity test
- `scipy.stats`: Linear regression for hedge ratio estimation
- `yfinance`: Historical price data
- `plotly`: Interactive visualizations

**Why Engle-Granger:**
- Industry standard for pairwise cointegration
- Intuitive economic interpretation (hedge ratio = beta)
- Computationally simple vs. Johansen (good for 2-asset case)

## References

### Academic Foundation
- Engle, R. F. & Granger, C. W. J. (1987). "Co-integration and Error Correction"
- Gatev, E., Goetzmann, W. N., & Rouwenhorst, K. G. (2006). "Pairs Trading: Performance of a Relative-Value Arbitrage Rule"
- Do, B. & Faff, R. (2010). "Does Simple Pairs Trading Still Work?"

### Practical Resources
- [QuantConnect Pairs Trading Tutorial](https://www.quantconnect.com/tutorials/strategy-library/pairs-trading-with-stocks)
- [Statsmodels Cointegration Docs](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.coint.html)

## Author

**Elaine Yao**  
Sophomore, University of Chicago | CS & Economics

---

*This project demonstrates quantitative rigor and statistical validation. The negative result teaches more than a cherry-picked winning backtest. Not investment advice.*
```
