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
4. **[Monthly Returns](visualizations/monthly_returns_heatmap.html)**: Inconsistent P&L distribution

## Installation & Usage
```bash