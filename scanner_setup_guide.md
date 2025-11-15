# Stock Scanner Setup Guide

## Quick Start (5 Minutes)

### Step 1: Install Python

**Windows:**
1. Download Python from python.org
2. Run installer
3. ✓ Check "Add Python to PATH"
4. Click "Install Now"

**Mac:**
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### Step 2: Install Required Libraries

Open Terminal/Command Prompt and run:

```bash
pip install yfinance pandas numpy matplotlib requests
```

If you get permission errors, try:
```bash
pip install --user yfinance pandas numpy matplotlib requests
```

### Step 3: Download the Scanner

Save the `stock_scanner.py` file to your computer (e.g., Desktop or Documents folder).

### Step 4: Run the Scanner

**Windows:**
1. Open Command Prompt
2. Navigate to the folder: `cd Desktop` (or wherever you saved it)
3. Run: `python stock_scanner.py`

**Mac/Linux:**
1. Open Terminal
2. Navigate to the folder: `cd Desktop`
3. Run: `python3 stock_scanner.py`

### Step 5: Review Results

The scanner will:
1. Download S&P 500 stock list
2. Analyze each stock (takes 5-10 minutes)
3. Display results in terminal
4. Save results to CSV file

---

## Understanding the Scanner

### What It Does

The scanner analyzes stocks based on these criteria:

1. **Price Position (30 points)**
   - Above 20 EMA: +10 points
   - Above 50 EMA: +10 points
   - Above 200 EMA: +10 points

2. **EMA Alignment (10 points)**
   - 20 EMA > 50 EMA > 200 EMA: +10 points

3. **RSI (15 points)**
   - RSI 40-70 (optimal): +15 points
   - RSI 30-80 (acceptable): +5 points

4. **MACD (15 points)**
   - MACD > Signal: +10 points
   - MACD > 0: +5 points

5. **Volume (10 points)**
   - Volume > 20-day average: +10 points

6. **Momentum (10 points)**
   - Positive weekly gain: +10 points

**Total Score: 0-100**
- 90-100: Extremely strong uptrend
- 80-89: Very strong uptrend
- 70-79: Strong uptrend
- 60-69: Moderate uptrend
- Below 60: Not included in results

### Filters Applied

The scanner automatically filters out:
- Penny stocks (< $5)
- Low volume stocks (< 500K average)
- Stocks without enough data
- Stocks not meeting minimum score

---

## Customizing the Scanner

### Scan Different Stocks

**Option 1: Scan Custom List**

Edit `stock_scanner.py` and uncomment these lines:

```python
# Around line 280
custom_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
scanner = StockScanner(stock_list=custom_tickers)
```

**Option 2: Scan Specific Sectors**

```python
# Tech stocks
tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD', 'INTC']

# Financial stocks
financial_stocks = ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C']

# Healthcare stocks
healthcare_stocks = ['JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'MRK']

scanner = StockScanner(stock_list=tech_stocks)
```

### Adjust Minimum Score

```python
# More selective (fewer results, higher quality)
results = scanner.scan(min_score=80, max_results=20)

# Less selective (more results, lower quality)
results = scanner.scan(min_score=50, max_results=100)
```

### Change Filters

Edit the `check_uptrend_criteria` method:

```python
# Change minimum price
if current_price < 10:  # Instead of 5
    return None

# Change minimum volume
if avg_volume < 1000000:  # Instead of 500000
    return None

# Adjust RSI range
if 50 <= latest['RSI'] <= 65:  # Instead of 40-70
    score += 15
```

---

## Automating the Scanner

### Run Daily Automatically

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 6:00 PM (after market close)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\stock_scanner.py`

**Mac/Linux (Cron):**

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 6 PM)
0 18 * * * cd /path/to/scanner && python3 stock_scanner.py
```

### Email Results

Add this to the scanner:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(results_df):
    """Send scan results via email"""
    
    # Email configuration
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # Use app-specific password
    receiver_email = "your_email@gmail.com"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Stock Scanner Results - {datetime.now().strftime('%Y-%m-%d')}"
    
    # Create body
    body = f"Found {len(results_df)} stocks in uptrends:\n\n"
    body += results_df.to_string()
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Add to main() function
if not results.empty:
    send_email_alert(results)
```

---

## Advanced Features

### Add More Indicators

```python
def calculate_adx(self, data, period=14):
    """Calculate Average Directional Index"""
    high = data['High']
    low = data['Low']
    close = data['Close']
    
    # Calculate True Range
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calculate Directional Movement
    up_move = high - high.shift()
    down_move = low.shift() - low
    
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
    
    # Calculate ADX
    atr = tr.rolling(period).mean()
    plus_di = 100 * (pd.Series(plus_dm).rolling(period).mean() / atr)
    minus_di = 100 * (pd.Series(minus_dm).rolling(period).mean() / atr)
    
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(period).mean()
    
    return adx

# Use in check_uptrend_criteria
data['ADX'] = self.calculate_adx(data)
if latest['ADX'] > 25:
    score += 10
    criteria_met.append(f"Strong trend (ADX: {latest['ADX']:.1f})")
```

### Add Fundamental Filters

```python
def check_fundamentals(self, ticker):
    """Check basic fundamental criteria"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Market cap > $1B
        if info.get('marketCap', 0) < 1_000_000_000:
            return False
        
        # Positive earnings
        if info.get('trailingEps', 0) <= 0:
            return False
        
        # Reasonable P/E ratio
        pe_ratio = info.get('trailingPE', 999)
        if pe_ratio > 100 or pe_ratio < 0:
            return False
        
        return True
    except:
        return True  # If can't get data, don't filter out
```

### Create Sector Scanner

```python
def scan_by_sector(self, sector):
    """Scan stocks in a specific sector"""
    
    sector_map = {
        'technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD', 'INTC', 'CSCO', 'ORCL', 'IBM'],
        'finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC', 'TFC', 'SCHW'],
        'healthcare': ['JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'MRK', 'ABT', 'DHR', 'BMY', 'AMGN'],
        'consumer': ['AMZN', 'WMT', 'HD', 'MCD', 'NKE', 'SBUX', 'TGT', 'LOW', 'TJX', 'DG'],
        'energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO', 'OXY', 'HAL']
    }
    
    if sector.lower() in sector_map:
        self.stock_list = sector_map[sector.lower()]
        return self.scan()
    else:
        print(f"Sector '{sector}' not found. Available: {list(sector_map.keys())}")
        return pd.DataFrame()
```

---

## Troubleshooting

### Common Issues

**Issue: "Module not found" error**
```bash
# Solution: Install the missing module
pip install module_name
```

**Issue: "Permission denied"**
```bash
# Solution: Use --user flag
pip install --user yfinance pandas numpy
```

**Issue: Scanner is very slow**
```python
# Solution: Scan fewer stocks
custom_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
scanner = StockScanner(stock_list=custom_list)
```

**Issue: No results found**
```python
# Solution: Lower the minimum score
results = scanner.scan(min_score=50)  # Instead of 60
```

**Issue: "Rate limit exceeded"**
```python
# Solution: Add delays between requests
import time
time.sleep(0.5)  # Add in the scan loop
```

---

## Best Practices

### Daily Routine

1. **Run scanner after market close** (4:00 PM ET)
2. **Review top 10-20 results**
3. **Manually verify on charts**
4. **Add best setups to watchlist**
5. **Set price alerts**
6. **Wait for entry signals**

### What to Do With Results

**Don't:**
- Buy immediately after scan
- Trade every result
- Ignore risk management
- Skip manual verification

**Do:**
- Build a watchlist
- Wait for pullbacks
- Verify trends on charts
- Check for news/catalysts
- Set proper stop losses
- Calculate position sizes

### Combining With Manual Analysis

Scanner finds opportunities → You verify and execute

1. **Scanner identifies** stocks meeting technical criteria
2. **You review** charts for clean price action
3. **You check** fundamentals and news
4. **You wait** for proper entry signals
5. **You execute** with proper risk management

---

## Next Steps

1. **Install and run** the scanner
2. **Review results** and familiarize yourself with output
3. **Customize** for your trading style
4. **Automate** to run daily
5. **Integrate** with your trading workflow

Remember: The scanner is a tool to find opportunities. Your analysis and risk management determine success!