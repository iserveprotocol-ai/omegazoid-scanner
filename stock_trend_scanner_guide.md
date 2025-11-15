# Complete Guide: Finding and Monitoring Uptrending Stocks

## Table of Contents
1. [Overview: Why Automated Screening Matters](#overview)
2. [Best Free Stock Screening Tools](#free-tools)
3. [Technical Criteria for Identifying Uptrends](#criteria)
4. [Building Your Own Python Stock Scanner](#python-scanner)
5. [Setting Up Automated Alerts](#alerts)
6. [Screening Strategies by Trading Style](#strategies)
7. [Interpreting Scanner Results](#interpreting)
8. [Common Pitfalls and How to Avoid Them](#pitfalls)

---

## Overview: Why Automated Screening Matters {#overview}

Manually reviewing thousands of stocks daily is impossible. Automated screening allows you to:

- **Save Time:** Screen thousands of stocks in seconds
- **Remove Emotion:** Objective criteria eliminate bias
- **Find Opportunities Early:** Catch trends before they become obvious
- **Stay Consistent:** Apply the same criteria every time
- **Monitor Multiple Markets:** Track stocks, crypto, forex simultaneously

### The Two Approaches

**1. Use Existing Screening Tools (Fastest)**
- Free and paid platforms with built-in screeners
- No coding required
- Limited customization
- Great for beginners

**2. Build Your Own Scanner (Most Powerful)**
- Complete customization
- Automated alerts
- Integration with your trading system
- Requires basic Python knowledge

We'll cover both approaches in this guide.

---

## Best Free Stock Screening Tools {#free-tools}

### 1. TradingView (Highly Recommended)

**Why It's Great:**
- Powerful stock screener with technical filters
- Real-time data for most markets
- Custom alerts
- Beautiful charts
- Free tier available

**How to Use for Trend Screening:**

1. Go to TradingView.com → Stock Screener
2. Set these filters:
   - **Market Cap:** > $500M (avoid penny stocks)
   - **Volume:** > 500K (ensure liquidity)
   - **Price:** > $5 (avoid low-quality stocks)
   - **Technical Filters:**
     - Price above 50 SMA
     - Price above 200 SMA
     - RSI between 40-70 (not overbought)
     - MACD above signal line
     - Volume > 20-day average

3. Sort by: Relative Strength or % Change
4. Save as a custom screener

**Pro Tip:** Create multiple screeners for different strategies (swing trading, position trading, breakouts, etc.)

### 2. Finviz (Free Stock Screener)

**Why It's Great:**
- Completely free
- Simple interface
- Pre-built technical screens
- Heat maps and visualizations

**How to Use:**

1. Go to Finviz.com → Screener
2. Select "Technical" tab
3. Use these filters:
   - **Price:** Over $5
   - **Average Volume:** Over 500K
   - **Pattern:** Horizontal S/R or Channel Up
   - **SMA20:** Price above SMA20
   - **SMA50:** Price above SMA50
   - **SMA200:** Price above SMA200
   - **RSI (14):** 40 to 70

4. Click "Charts" to see visual results
5. Export results to CSV

**Pre-Built Screens to Try:**
- "Top Gainers" (but wait for pullbacks!)
- "New High"
- "Horizontal S/R"
- "TL Resistance"

### 3. Yahoo Finance Screener

**Why It's Great:**
- Completely free
- No account required
- Good for fundamental + technical screening
- Easy to use

**How to Use:**

1. Go to finance.yahoo.com/screener
2. Create custom screen with:
   - **Market Cap:** Large Cap or Mid Cap
   - **Price:** $5 - $10,000
   - **Volume:** > 500,000
   - **% Change:** Positive (optional)
   - **Technical:** Add custom technical criteria

3. Save and run daily

### 4. ThinkorSwim (TD Ameritrade)

**Why It's Great:**
- Professional-grade platform
- Advanced scanning capabilities
- Free with TD Ameritrade account
- Real-time data

**How to Use:**

1. Open ThinkorSwim → Scan tab
2. Use "Stock Hacker"
3. Add filters:
   - Price above 50-day SMA
   - Price above 200-day SMA
   - Volume > 500K
   - RSI between 40-70
   - MACD Bullish

4. Save as custom scan
5. Run automatically

### 5. StockCharts.com

**Why It's Great:**
- Excellent charting
- Pre-defined scans
- Technical focus
- Free tier available

**Pre-Built Scans:**
- "Bullish Percent Index"
- "New Highs"
- "Moving Average Crossovers"
- "Relative Strength Leaders"

### Comparison Table

| Tool | Cost | Ease of Use | Customization | Best For |
|------|------|-------------|---------------|----------|
| TradingView | Free/Paid | Easy | High | All traders |
| Finviz | Free | Very Easy | Medium | Beginners |
| Yahoo Finance | Free | Easy | Low | Quick scans |
| ThinkorSwim | Free* | Medium | Very High | Active traders |
| StockCharts | Free/Paid | Medium | High | Technical traders |

*Requires TD Ameritrade account

---

## Technical Criteria for Identifying Uptrends {#criteria}

### The Core Trend Filters

These are the essential criteria that define an uptrend:

#### 1. Price Above Moving Averages

**Why It Matters:**
Moving averages show the average price over time. When price is above key MAs, it indicates bullish momentum.

**Criteria:**
- Price > 20-day EMA (short-term trend)
- Price > 50-day EMA (medium-term trend)
- Price > 200-day EMA (long-term trend)

**Ideal Setup:**
- 20 EMA > 50 EMA > 200 EMA (all aligned upward)
- Price bouncing off 20 or 50 EMA (pullback entry)

#### 2. Higher Highs and Higher Lows

**Why It Matters:**
This is the definition of an uptrend. Each peak should be higher than the last, and each valley should be higher than the last.

**How to Screen:**
- Look for stocks making new 52-week highs
- Or stocks within 10% of 52-week highs
- Avoid stocks making new lows

#### 3. Volume Confirmation

**Why It Matters:**
Volume shows conviction. Uptrends with increasing volume are more sustainable.

**Criteria:**
- Average volume > 500K shares (liquidity)
- Volume increasing on up days
- Volume decreasing on down days
- Current volume > 20-day average

#### 4. RSI (Relative Strength Index)

**Why It Matters:**
RSI shows momentum and helps avoid overbought conditions.

**Criteria:**
- RSI > 50 (bullish momentum)
- RSI < 70 (not overbought)
- Ideal range: 40-65 (room to run)

**Avoid:**
- RSI > 80 (extremely overbought)
- RSI < 30 (bearish momentum)

#### 5. MACD (Moving Average Convergence Divergence)

**Why It Matters:**
MACD shows trend direction and momentum shifts.

**Criteria:**
- MACD line above signal line (bullish)
- MACD above zero line (strong uptrend)
- Histogram expanding (increasing momentum)

**Ideal Setup:**
- Recent bullish crossover (MACD crossed above signal)
- Histogram turning positive

#### 6. Relative Strength

**Why It Matters:**
Stocks that outperform the market tend to continue outperforming.

**Criteria:**
- Relative Strength vs. S&P 500 > 70
- Outperforming sector peers
- Positive price momentum

### Advanced Filters

#### 7. Bollinger Bands

**Criteria:**
- Price riding upper Bollinger Band (strong trend)
- Or price bouncing off middle band (pullback entry)
- Bands expanding (increasing volatility)

#### 8. ADX (Average Directional Index)

**Why It Matters:**
ADX measures trend strength, not direction.

**Criteria:**
- ADX > 25 (strong trend)
- ADX > 40 (very strong trend)
- +DI above -DI (uptrend)

#### 9. Support and Resistance

**Criteria:**
- Price above key resistance levels
- Clear support levels below
- No major overhead resistance

### The Complete Uptrend Filter

**Combine all criteria for highest probability setups:**

```
✓ Price > 20 EMA > 50 EMA > 200 EMA
✓ Making higher highs and higher lows
✓ Volume > 500K average
✓ Volume increasing on up days
✓ RSI between 40-70
✓ MACD above signal line
✓ MACD above zero line
✓ Relative Strength > 70
✓ ADX > 25
✓ No major resistance overhead
```

**Stocks meeting all criteria = Highest probability uptrends**

### Screening by Trading Style

**Day Trading (Short-term):**
- Focus on: Volume, RSI, MACD
- Time frame: 5-min, 15-min charts
- Criteria: High volume, strong momentum

**Swing Trading (Medium-term):**
- Focus on: Moving averages, RSI, support/resistance
- Time frame: Daily charts
- Criteria: Pullbacks in uptrends

**Position Trading (Long-term):**
- Focus on: 200 EMA, relative strength, fundamentals
- Time frame: Weekly charts
- Criteria: Strong long-term trends

---

## Building Your Own Python Stock Scanner {#python-scanner}

Now let's build a custom scanner that you can run automatically!

### Prerequisites

**What You Need:**
- Python 3.8 or higher
- Basic command line knowledge
- 30 minutes to set up

**Why Build Your Own:**
- Complete customization
- Automated daily scans
- Email/SMS alerts
- Free (no subscription fees)
- Learn valuable skills

### Step 1: Install Required Libraries

Open your terminal/command prompt and run:

```bash
pip install yfinance pandas numpy ta-lib matplotlib requests
```

**What each library does:**
- `yfinance`: Downloads stock data from Yahoo Finance
- `pandas`: Data manipulation
- `numpy`: Mathematical operations
- `ta-lib`: Technical indicators (optional, can use pandas-ta instead)
- `matplotlib`: Charting
- `requests`: API calls for alerts

**Alternative (if ta-lib installation fails):**
```bash
pip install yfinance pandas numpy pandas-ta matplotlib requests
```

### Step 2: Basic Stock Scanner Script

I'll create a complete, working scanner for you in the next file!

---

## Setting Up Automated Alerts {#alerts}

### Email Alerts

**Using Gmail:**

1. Enable 2-factor authentication on your Google account
2. Generate an app-specific password
3. Use the email alert code in the scanner

**Using Telegram:**

1. Create a Telegram bot via @BotFather
2. Get your bot token
3. Get your chat ID
4. Use Telegram API for alerts

### SMS Alerts

**Using Twilio:**

1. Sign up for Twilio (free trial)
2. Get your Account SID and Auth Token
3. Get a Twilio phone number
4. Integrate with scanner

### Push Notifications

**Using Pushover:**

1. Sign up for Pushover ($5 one-time)
2. Get your user key and API token
3. Integrate with scanner

---

## Screening Strategies by Trading Style {#strategies}

### Strategy 1: Pullback in Uptrend (Swing Trading)

**Criteria:**
- Price > 50 EMA and 200 EMA
- Price pulled back to 20 or 50 EMA
- RSI between 40-50 (reset from overbought)
- MACD still positive
- Volume declining on pullback

**When to Enter:**
- Price bounces off EMA with volume
- RSI turns back up
- MACD histogram expands

### Strategy 2: Breakout Scanner (Momentum Trading)

**Criteria:**
- Price breaking above resistance
- Volume > 2x average
- RSI > 60
- MACD bullish crossover
- No major resistance overhead

**When to Enter:**
- On breakout with volume
- Or on retest of breakout level

### Strategy 3: New High Scanner (Position Trading)

**Criteria:**
- Making new 52-week high
- Price > all moving averages
- Relative strength > 80
- ADX > 25
- Strong fundamentals

**When to Enter:**
- On first pullback after new high
- Or on continuation after consolidation

### Strategy 4: Moving Average Cross (Trend Following)

**Criteria:**
- 50 EMA crossing above 200 EMA (Golden Cross)
- Or 20 EMA crossing above 50 EMA
- Volume increasing
- RSI > 50
- Price above both MAs

**When to Enter:**
- On the crossover
- Or on first pullback after cross

---

## Interpreting Scanner Results {#interpreting}

### What to Do With Your Scan Results

**Step 1: Review the List**
- Scanner will return 10-100+ stocks
- Don't try to trade them all
- Focus on top 5-10 setups

**Step 2: Manual Chart Review**
- Open charts for each stock
- Verify the trend visually
- Check for clean price action
- Look for clear support/resistance

**Step 3: Fundamental Check**
- Quick review of company
- Any recent news?
- Earnings coming up?
- Sector strength?

**Step 4: Create Watchlist**
- Add best setups to watchlist
- Set price alerts
- Wait for entry signals

**Step 5: Plan Your Trade**
- Determine entry price
- Calculate stop loss
- Set profit targets
- Calculate position size

### Red Flags to Watch For

**Avoid These Stocks:**
- Low volume (< 500K average)
- Penny stocks (< $5)
- Parabolic moves (likely to reverse)
- Stocks with major resistance overhead
- Stocks with negative news
- Stocks in weak sectors

### Quality Over Quantity

**Better to have:**
- 5 high-quality setups you understand
- Than 50 mediocre setups you don't

**Focus on:**
- Clean trends
- Clear support/resistance
- Good risk-reward ratios
- Stocks you can monitor

---

## Common Pitfalls and How to Avoid Them {#pitfalls}

### Pitfall #1: Over-Optimization

**The Problem:**
Adding too many filters results in zero results or only perfect setups that rarely occur.

**The Solution:**
- Start with basic filters
- Add complexity gradually
- Test with historical data
- Balance specificity with opportunity

### Pitfall #2: Ignoring Market Context

**The Problem:**
Scanning for uptrends during a bear market leads to false signals.

**The Solution:**
- Check overall market trend first (S&P 500)
- Adjust criteria for market conditions
- Be more selective in bear markets
- Consider inverse/short setups in downtrends

### Pitfall #3: Not Verifying Results

**The Problem:**
Blindly trading scanner results without manual verification.

**The Solution:**
- Always review charts manually
- Verify the trend visually
- Check for news/catalysts
- Confirm with multiple time frames

### Pitfall #4: Chasing Scanner Results

**The Problem:**
Buying stocks immediately after they appear on scanner (often too late).

**The Solution:**
- Use scanner to build watchlist
- Wait for proper entry signals
- Look for pullbacks
- Be patient

### Pitfall #5: Ignoring Risk Management

**The Problem:**
Finding great stocks but not managing position size or stops.

**The Solution:**
- Calculate position size before entering
- Set stop losses based on technical levels
- Never risk more than 1-2% per trade
- Have an exit plan

---

## Next Steps

1. **Choose Your Approach:**
   - Start with free tools (TradingView, Finviz)
   - Or build your own Python scanner

2. **Define Your Criteria:**
   - What type of trends are you looking for?
   - What's your trading style?
   - What time frame?

3. **Test Your Scanner:**
   - Run it daily for a week
   - Track results
   - Refine criteria

4. **Build Your Watchlist:**
   - Add best setups
   - Set alerts
   - Wait for entries

5. **Start Small:**
   - Paper trade first
   - Then small positions
   - Scale up as you prove consistency

---

## Conclusion

Finding uptrending stocks doesn't have to be complicated. With the right tools and criteria, you can scan thousands of stocks in minutes and identify high-probability setups.

**Key Takeaways:**

1. Use free tools like TradingView or Finviz to start
2. Focus on core criteria: Price > MAs, RSI, MACD, Volume
3. Build your own scanner for maximum customization
4. Always verify results manually
5. Quality over quantity - focus on best setups
6. Combine screening with proper risk management

The scanner finds opportunities. Your analysis and risk management determine success.

Ready to build your Python scanner? Let's create it in the next file!