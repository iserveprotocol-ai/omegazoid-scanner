#!/usr/bin/env python3
"""
Crypto Trend Scanner
Automatically scans for cryptocurrencies in uptrends based on technical criteria
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import requests
import json
import os
import time
warnings.filterwarnings('ignore')

# CoinMarketCap API Configuration
# For deployment: Set CMC_API_KEY as environment variable
CMC_API_KEY = os.environ.get('CMC_API_KEY', '24fb5bf708c346b099c9900c3b1082bc')
CMC_API_URL = 'https://pro-api.coinmarketcap.com/v1'

# Stablecoins to exclude from scanning (no volatility)
STABLECOINS = {
    'USDT-USD', 'USDC-USD', 'BUSD-USD', 'DAI-USD', 'USDD-USD', 'TUSD-USD', 
    'USDP-USD', 'GUSD-USD', 'FRAX-USD', 'USDN-USD', 'FEI-USD', 'LUSD-USD',
    'SUSD-USD', 'USTC-USD', 'HUSD-USD', 'USDK-USD', 'USDX-USD', 'RSV-USD',
    'MUSD-USD', 'DUSD-USD', 'CUSD-USD', 'OUSD-USD', 'EUROC-USD', 'EURT-USD',
    'XSGD-USD', 'GYEN-USD', 'USDS-USD', 'USDE-USD', 'PYUSD-USD', 'FDUSD-USD'
}

# Crypto sector classification
CRYPTO_SECTORS = {
    # Layer 1 Blockchains
    'BTC-USD': 'Layer 1', 'ETH-USD': 'Layer 1', 'SOL-USD': 'Layer 1', 'ADA-USD': 'Layer 1',
    'AVAX-USD': 'Layer 1', 'DOT-USD': 'Layer 1', 'ATOM-USD': 'Layer 1', 'NEAR-USD': 'Layer 1',
    'ALGO-USD': 'Layer 1', 'XTZ-USD': 'Layer 1', 'ETC-USD': 'Layer 1', 'BCH-USD': 'Layer 1',
    'LTC-USD': 'Layer 1', 'XLM-USD': 'Layer 1', 'XRP-USD': 'Layer 1', 'TRX-USD': 'Layer 1',
    'ICP-USD': 'Layer 1', 'FIL-USD': 'Layer 1', 'APT-USD': 'Layer 1', 'SUI-USD': 'Layer 1',
    'SEI-USD': 'Layer 1', 'INJ-USD': 'Layer 1', 'TON-USD': 'Layer 1', 'KLAY-USD': 'Layer 1',
    'FTM-USD': 'Layer 1', 'NEO-USD': 'Layer 1', 'WAVES-USD': 'Layer 1', 'QTUM-USD': 'Layer 1',
    
    # Layer 2 / Scaling
    'MATIC-USD': 'Layer 2', 'ARB-USD': 'Layer 2', 'OP-USD': 'Layer 2', 'IMX-USD': 'Layer 2',
    'METIS-USD': 'Layer 2', 'STRK-USD': 'Layer 2', 'MANTA-USD': 'Layer 2',
    
    # DeFi
    'UNI-USD': 'DeFi', 'AAVE-USD': 'DeFi', 'CRV-USD': 'DeFi', 'COMP-USD': 'DeFi',
    'SUSHI-USD': 'DeFi', 'SNX-USD': 'DeFi', 'MKR-USD': 'DeFi', 'YFI-USD': 'DeFi',
    'CAKE-USD': 'DeFi', 'LRC-USD': 'DeFi', 'RUNE-USD': 'DeFi', 'KAVA-USD': 'DeFi',
    'CELO-USD': 'DeFi', 'BNT-USD': 'DeFi', 'BAL-USD': 'DeFi', 'LDO-USD': 'DeFi',
    'GMX-USD': 'DeFi', 'PENDLE-USD': 'DeFi', 'DYDX-USD': 'DeFi', 'JUP-USD': 'DeFi',
    'RDNT-USD': 'DeFi', 'VELODROME-USD': 'DeFi', 'CVX-USD': 'DeFi', 'FXS-USD': 'DeFi',
    
    # Meme Coins
    'DOGE-USD': 'Meme', 'SHIB-USD': 'Meme', 'PEPE-USD': 'Meme', 'BONK-USD': 'Meme',
    'FLOKI-USD': 'Meme', 'WIF-USD': 'Meme', 'BOME-USD': 'Meme', 'WEN-USD': 'Meme',
    'MYRO-USD': 'Meme', 'DEGEN-USD': 'Meme', 'MEME-USD': 'Meme', 'NEIRO-USD': 'Meme',
    'TURBO-USD': 'Meme', 'GOAT-USD': 'Meme', 'PNUT-USD': 'Meme', 'ACT-USD': 'Meme',
    
    # Gaming / Metaverse
    'SAND-USD': 'Gaming', 'MANA-USD': 'Gaming', 'AXS-USD': 'Gaming', 'GALA-USD': 'Gaming',
    'ENJ-USD': 'Gaming', 'ILV-USD': 'Gaming', 'YGG-USD': 'Gaming', 'MAGIC-USD': 'Gaming',
    'VOXEL-USD': 'Gaming', 'ALICE-USD': 'Gaming', 'TLM-USD': 'Gaming', 'SLP-USD': 'Gaming',
    'PORTAL-USD': 'Gaming', 'PIXEL-USD': 'Gaming', 'BEAM-USD': 'Gaming', 'PRIME-USD': 'Gaming',
    
    # AI / Data
    'RNDR-USD': 'AI', 'FET-USD': 'AI', 'AGIX-USD': 'AI', 'GRT-USD': 'AI',
    'OCEAN-USD': 'AI', 'TAO-USD': 'AI', 'WLD-USD': 'AI', 'ARKM-USD': 'AI',
    'AIOZ-USD': 'AI', 'NMR-USD': 'AI', 'ROSE-USD': 'AI',
    
    # Oracles / Infrastructure
    'LINK-USD': 'Oracle', 'BAND-USD': 'Oracle', 'API3-USD': 'Oracle', 'TRB-USD': 'Oracle',
    'PYTH-USD': 'Oracle', 'DIA-USD': 'Oracle',
    
    # Privacy
    'XMR-USD': 'Privacy', 'ZEC-USD': 'Privacy', 'DASH-USD': 'Privacy', 'SCRT-USD': 'Privacy',
    
    # Storage
    'FIL-USD': 'Storage', 'AR-USD': 'Storage', 'STORJ-USD': 'Storage',
    
    # Exchange Tokens
    'BNB-USD': 'Exchange', 'KCS-USD': 'Exchange', 'OKB-USD': 'Exchange',
    
    # NFT / Collectibles
    'BLUR-USD': 'NFT', 'LOOKS-USD': 'NFT', 'APE-USD': 'NFT',
}

class CryptoScanner:
    """
    A comprehensive crypto scanner for identifying uptrending cryptocurrencies
    """
    
    def __init__(self, crypto_list=None, use_cmc=True):
        """
        Initialize the scanner
        
        Args:
            crypto_list: List of crypto tickers to scan. If None, uses top cryptos
            use_cmc: If True, fetch top cryptos from CoinMarketCap API
        """
        self.cmc_data = {}  # Initialize before getting crypto list
        
        if crypto_list:
            self.crypto_list = crypto_list
        elif use_cmc:
            self.crypto_list = self.get_top_cryptos_from_cmc()
        else:
            self.crypto_list = self.get_top_cryptos()
        self.results = []
        
    def get_top_cryptos(self):
        """
        Get list of top cryptocurrencies (USD pairs)
        Fallback list if CoinMarketCap API fails
        Focus on most reliable/liquid cryptos for Yahoo Finance
        """
        # Reliable top 50 cryptos that Yahoo Finance consistently provides data for
        cryptos = [
            # Top 20 - Most reliable
            'BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'XRP-USD', 'ADA-USD',
            'DOGE-USD', 'AVAX-USD', 'DOT-USD', 'MATIC-USD', 'LTC-USD', 'LINK-USD',
            'UNI-USD', 'ATOM-USD', 'XLM-USD', 'ALGO-USD', 'VET-USD', 'ICP-USD',
            'FIL-USD', 'AAVE-USD',
            # Additional reliable 30
            'ETC-USD', 'BCH-USD', 'XMR-USD', 'APT-USD', 'NEAR-USD', 'GRT-USD',
            'CRV-USD', 'SNX-USD', 'COMP-USD', 'SUSHI-USD', 'MKR-USD', 'YFI-USD',
            'OP-USD', 'ARB-USD', 'LDO-USD', 'IMX-USD', 'INJ-USD', 'RUNE-USD',
            'DYDX-USD', 'RNDR-USD', 'STX-USD', 'KAVA-USD', 'AXS-USD', 'ENJ-USD',
            'CHZ-USD', 'ZEC-USD', 'DASH-USD', 'CAKE-USD', 'LRC-USD', 'BAT-USD'
        ]
        # Remove stablecoins from the list
        cryptos = [c for c in cryptos if c not in STABLECOINS]
        print(f"✓ Using fallback list of {len(cryptos)} major cryptocurrencies")
        return cryptos
    
    def get_top_cryptos_from_cmc(self, limit=250, filter_kraken=False, filter_cryptocom=False):
        """
        Get top cryptocurrencies from CoinMarketCap API by market cap
        Returns Yahoo Finance compatible tickers
        
        Args:
            limit: Number of cryptos to fetch (default: 250)
            filter_kraken: If True, only return cryptos tradable on Kraken
            filter_cryptocom: If True, only return cryptos tradable on Crypto.com
        """
        try:
            print(f"Fetching top {limit} cryptocurrencies from CoinMarketCap...")
            
            headers = {
                'X-CMC_PRO_API_KEY': CMC_API_KEY,
                'Accept': 'application/json'
            }
            
            params = {
                'start': '1',
                'limit': str(limit),
                'convert': 'USD'
            }
            
            response = requests.get(
                f'{CMC_API_URL}/cryptocurrency/listings/latest',
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                cryptos = []
                
                # Store CMC data for additional info
                for crypto in data['data']:
                    symbol = crypto['symbol']
                    ticker = f"{symbol}-USD"
                    
                    # Skip stablecoins
                    if ticker in STABLECOINS:
                        continue
                    
                    cryptos.append(ticker)
                    
                    # Store market cap and other data
                    self.cmc_data[ticker] = {
                        'name': crypto['name'],
                        'market_cap': crypto['quote']['USD']['market_cap'],
                        'market_cap_rank': crypto['cmc_rank'],
                        'volume_24h': crypto['quote']['USD']['volume_24h'],
                        'percent_change_24h': crypto['quote']['USD']['percent_change_24h'],
                        'percent_change_7d': crypto['quote']['USD']['percent_change_7d'],
                        'percent_change_30d': crypto['quote']['USD']['percent_change_30d']
                    }
                
                print(f"✓ Successfully fetched {len(cryptos)} cryptos from CoinMarketCap")
                print(f"  Top 5: {', '.join([c.replace('-USD', '') for c in cryptos[:5]])}")
                
                # Filter for Kraken if requested
                if filter_kraken:
                    kraken_pairs = self.get_kraken_tradable_pairs()
                    if kraken_pairs:
                        original_count = len(cryptos)
                        cryptos = [c for c in cryptos if c.replace('-USD', '') in kraken_pairs]
                        print(f"✓ Filtered to {len(cryptos)} cryptos tradable on Kraken (from {original_count})")
                
                # Filter for Crypto.com if requested
                if filter_cryptocom:
                    cryptocom_pairs = self.get_cryptocom_tradable_pairs()
                    if cryptocom_pairs:
                        original_count = len(cryptos)
                        cryptos = [c for c in cryptos if c.replace('-USD', '') in cryptocom_pairs]
                        print(f"✓ Filtered to {len(cryptos)} cryptos tradable on Crypto.com (from {original_count})")
                
                return cryptos
            else:
                print(f"⚠ CoinMarketCap API error (Status {response.status_code}), using fallback list")
                return self.get_top_cryptos()
                
        except Exception as e:
            print(f"⚠ Error fetching from CoinMarketCap: {e}")
            print("  Using fallback crypto list")
            return self.get_top_cryptos()
    
    def get_cmc_info(self, ticker):
        """
        Get CoinMarketCap data for a specific ticker
        """
        return self.cmc_data.get(ticker, {})
    
    def get_crypto_sector(self, ticker):
        """
        Get sector/category for a crypto
        """
        return CRYPTO_SECTORS.get(ticker, 'Other')
    
    def get_fear_greed_index(self):
        """
        Get current Crypto Fear & Greed Index
        Returns value 0-100 and classification
        """
        try:
            response = requests.get('https://api.alternative.me/fng/?limit=1')
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    value = int(data['data'][0]['value'])
                    classification = data['data'][0]['value_classification']
                    return {'value': value, 'classification': classification}
        except:
            pass
        return None
    
    def get_bitcoin_dominance(self):
        """
        Get Bitcoin dominance percentage from CoinMarketCap
        """
        try:
            headers = {
                'X-CMC_PRO_API_KEY': CMC_API_KEY,
                'Accept': 'application/json'
            }
            
            response = requests.get(
                f'{CMC_API_URL}/global-metrics/quotes/latest',
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                btc_dominance = data['data']['btc_dominance']
                eth_dominance = data['data']['eth_dominance']
                return {'btc': round(btc_dominance, 2), 'eth': round(eth_dominance, 2)}
        except:
            pass
        return None
    
    def calculate_position_size(self, account_size, risk_percent, entry_price, stop_loss_price):
        """
        Calculate position size based on risk management
        
        Args:
            account_size: Total trading account size in USD
            risk_percent: Percentage of account to risk (e.g., 1 or 2)
            entry_price: Entry price for the trade
            stop_loss_price: Stop loss price
            
        Returns:
            dict with position details
        """
        risk_amount = account_size * (risk_percent / 100)
        risk_per_unit = abs(entry_price - stop_loss_price)
        
        if risk_per_unit == 0:
            return None
        
        position_size_units = risk_amount / risk_per_unit
        position_value = position_size_units * entry_price
        
        return {
            'units': position_size_units,
            'value_usd': position_value,
            'risk_usd': risk_amount,
            'risk_per_unit': risk_per_unit
        }
    
    def calculate_profit_loss(self, entry_price, target_price, stop_loss_price, position_size_usd):
        """
        Calculate potential profit and loss in USD
        
        Args:
            entry_price: Entry price
            target_price: Take profit target
            stop_loss_price: Stop loss price
            position_size_usd: Position size in USD
            
        Returns:
            dict with P/L calculations
        """
        units = position_size_usd / entry_price
        
        potential_profit = (target_price - entry_price) * units
        potential_loss = (entry_price - stop_loss_price) * units
        profit_pct = ((target_price - entry_price) / entry_price) * 100
        loss_pct = ((entry_price - stop_loss_price) / entry_price) * 100
        
        return {
            'profit_usd': potential_profit,
            'loss_usd': potential_loss,
            'profit_pct': profit_pct,
            'loss_pct': loss_pct,
            'risk_reward': abs(potential_profit / potential_loss) if potential_loss != 0 else 0
        }
    
    def get_kraken_tradable_pairs(self):
        """
        Get list of crypto symbols tradable on Kraken (USD pairs)
        Returns set of symbols (e.g., {'BTC', 'ETH', ...})
        """
        try:
            response = requests.get('https://api.kraken.com/0/public/AssetPairs')
            if response.status_code == 200:
                data = response.json()
                if data.get('error') and len(data['error']) > 0:
                    print(f"⚠ Kraken API error: {data['error']}")
                    return None
                
                pairs = data.get('result', {})
                # Extract USD pairs only
                usd_symbols = set()
                for pair_name, pair_data in pairs.items():
                    # Check if it's a USD pair
                    if 'USD' in pair_name and 'quote' in pair_data:
                        base = pair_data.get('base', '')
                        quote = pair_data.get('quote', '')
                        
                        # Only USD quotes
                        if quote in ['ZUSD', 'USD']:
                            # Clean up symbol (remove X/Z prefixes Kraken uses)
                            clean_symbol = base.replace('X', '').replace('Z', '')
                            usd_symbols.add(clean_symbol)
                
                print(f"✓ Found {len(usd_symbols)} cryptos tradable on Kraken")
                return usd_symbols
            else:
                print(f"⚠ Kraken API returned status {response.status_code}")
                return None
        except Exception as e:
            print(f"⚠ Error fetching Kraken pairs: {e}")
            return None
    
    def get_cryptocom_tradable_pairs(self):
        """
        Get list of crypto symbols tradable on Crypto.com
        Uses a curated list of major cryptos supported on Crypto.com App
        Returns set of symbols (e.g., {'BTC', 'ETH', ...})
        """
        # Crypto.com supports 250+ cryptos - here's a comprehensive list of major ones
        # Based on their public listings as of 2024
        cryptocom_cryptos = {
            # Top 50 by market cap
            'BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'USDC', 'XRP', 'ADA', 'AVAX', 'DOGE',
            'TRX', 'DOT', 'MATIC', 'LINK', 'SHIB', 'UNI', 'LTC', 'BCH', 'ATOM', 'XLM',
            'ETC', 'FIL', 'HBAR', 'ICP', 'APT', 'ARB', 'NEAR', 'VET', 'ALGO', 'MANA',
            'SAND', 'AXS', 'THETA', 'AAVE', 'FTM', 'XTZ', 'EGLD', 'FLOW', 'CHZ', 'QNT',
            'MKR', 'RUNE', 'SNX', 'CRV', 'CAKE', 'ENJ', 'ZEC', 'XMR', 'DASH', 'NEO',
            
            # DeFi & Layer 2
            'OP', 'COMP', 'SUSHI', 'YFI', 'BAL', '1INCH', 'LRC', 'CELO', 'ZRX',
            'REN', 'KNC', 'BAND', 'OMG', 'GRT', 'ANKR', 'SKL', 'CELR', 'STORJ',
            
            # Gaming & Metaverse
            'GALA', 'IMX', 'ALICE', 'TLM', 'ILV', 'YGG', 'VOXEL', 'SUPER', 'HIGH',
            
            # Infrastructure
            'RNDR', 'FET', 'OCEAN', 'NMR', 'API3', 'AR', 'LPT', 'BAT', 'GNO',
            
            # Meme & Others
            'PEPE', 'FLOKI', 'ELON', 'BONK',
            
            # Additional major coins
            'WAVES', 'KAVA', 'ONE', 'IOST', 'QTUM', 'ICX', 'ZIL', 'ONT', 'RVN',
            'DCR', 'SC', 'LSK', 'STEEM', 'BNT', 'KMD', 'POLY', 'DOCK', 'STMX',
            'ENS', 'LDO', 'GMT', 'APE', 'BLUR', 'DYDX', 'PENDLE', 'MASK', 'ORDI'
        }
        
        print(f"✓ Found {len(cryptocom_cryptos)} cryptos tradable on Crypto.com (curated list)")
        return cryptocom_cryptos
    
    def calculate_adx(self, data, period=14):
        """Calculate Average Directional Index for trend strength"""
        try:
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
            
            # Calculate smoothed values
            atr = tr.rolling(period).mean()
            plus_di = 100 * (pd.Series(plus_dm, index=data.index).rolling(period).mean() / atr)
            minus_di = 100 * (pd.Series(minus_dm, index=data.index).rolling(period).mean() / atr)
            
            # Calculate DX and ADX
            dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
            adx = pd.Series(dx.values, index=data.index).rolling(period).mean()
            
            # Fill NaN values with 0
            adx = adx.fillna(0)
            plus_di = pd.Series(plus_di.values if hasattr(plus_di, 'values') else plus_di, index=data.index).fillna(0)
            minus_di = pd.Series(minus_di.values if hasattr(minus_di, 'values') else minus_di, index=data.index).fillna(0)
            
            return adx, plus_di, minus_di
        except Exception as e:
            # Return zeros if calculation fails
            return pd.Series(0, index=data.index), pd.Series(0, index=data.index), pd.Series(0, index=data.index)
    
    def calculate_atr(self, data, period=14):
        """Calculate Average True Range for volatility"""
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        atr = tr.rolling(period).mean()
        return atr
    
    def calculate_bollinger_bands(self, data, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        middle_band = data['Close'].rolling(period).mean()
        std = data['Close'].rolling(period).std()
        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)
        
        return upper_band, middle_band, lower_band
    
    def find_support_resistance(self, data, window=20):
        """Find key support and resistance levels"""
        # Find local highs and lows
        highs = data['High'].rolling(window=window, center=True).max()
        lows = data['Low'].rolling(window=window, center=True).min()
        
        # Current price
        current_price = data['Close'].iloc[-1]
        
        # Find nearest support (recent lows)
        recent_lows = data['Low'].tail(window * 2)
        support_levels = recent_lows[recent_lows < current_price].tail(3)
        nearest_support = support_levels.max() if len(support_levels) > 0 else data['Low'].min()
        
        # Find nearest resistance (recent highs)
        recent_highs = data['High'].tail(window * 2)
        resistance_levels = recent_highs[recent_highs > current_price].tail(3)
        nearest_resistance = resistance_levels.min() if len(resistance_levels) > 0 else data['High'].max()
        
        return nearest_support, nearest_resistance
    
    def check_volume_divergence(self, data, periods=5):
        """Detect volume divergence (warning sign)"""
        # Check if price is making higher highs but volume is declining
        recent_prices = data['Close'].tail(periods)
        recent_volumes = data['Volume'].tail(periods)
        
        price_trend_up = recent_prices.iloc[-1] > recent_prices.iloc[0]
        volume_trend_down = recent_volumes.iloc[-1] < recent_volumes.iloc[0]
        
        # Bearish divergence: price up, volume down
        has_divergence = price_trend_up and volume_trend_down
        
        return has_divergence
    
    def check_weekly_trend(self, ticker):
        """Check weekly timeframe for trend confirmation"""
        try:
            stock = yf.Ticker(ticker)
            weekly_data = stock.history(period='1y', interval='1wk')
            
            if len(weekly_data) < 20:
                return None
            
            # Calculate weekly EMAs
            weekly_data['EMA_10'] = weekly_data['Close'].ewm(span=10, adjust=False).mean()
            weekly_data['EMA_20'] = weekly_data['Close'].ewm(span=20, adjust=False).mean()
            
            latest = weekly_data.iloc[-1]
            
            # Check if weekly trend is bullish
            weekly_bullish = (latest['Close'] > latest['EMA_10'] > latest['EMA_20'])
            
            return weekly_bullish
        except:
            return None
        """Calculate Exponential Moving Average"""
        return data['Close'].ewm(span=period, adjust=False).mean()
    
    def calculate_ema(self, data, period):
        """Calculate Exponential Moving Average"""
        return data['Close'].ewm(span=period, adjust=False).mean()
    
    def calculate_rsi(self, data, period=14):
        """Calculate Relative Strength Index"""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data):
        """Calculate MACD"""
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        return macd, signal, histogram
    
    def check_uptrend_criteria(self, ticker):
        """
        Check if a crypto meets uptrend criteria with enhanced analysis
        
        Returns:
            dict: Results with score and details, or None if criteria not met
        """
        try:
            # Skip stablecoins
            if ticker in STABLECOINS:
                return None
            
            # Download data (6 months for better MA calculation)
            stock = yf.Ticker(ticker)
            data = stock.history(period='6mo')
            
            if len(data) < 100:  # Need enough data (reduced from 200)
                return None
            
            # Get current price and info
            current_price = data['Close'].iloc[-1]
            
            # Skip very low value cryptos (below $0.01)
            if current_price < 0.01:
                return None
            
            # Additional stablecoin check by price (anything between $0.95-$1.05 with low volatility)
            recent_high = data['High'].tail(30).max()
            recent_low = data['Low'].tail(30).min()
            price_range = recent_high - recent_low
            if 0.95 <= current_price <= 1.05 and price_range < 0.10:
                return None  # Likely a stablecoin
            
            # Calculate ATH and ATL from available data (6 months)
            ath_6mo = data['High'].max()
            atl_6mo = data['Low'].min()
            
            # Try to get longer-term data for more accurate ATH/ATL (max period available)
            try:
                long_data = stock.history(period='max')
                if len(long_data) > len(data):
                    ath_all_time = long_data['High'].max()
                    atl_all_time = long_data['Low'].min()
                else:
                    ath_all_time = ath_6mo
                    atl_all_time = atl_6mo
            except:
                # If max data fails, use 6mo data
                ath_all_time = ath_6mo
                atl_all_time = atl_6mo
            
            # Calculate distances from ATH and ATL
            distance_from_ath = ((current_price - ath_all_time) / ath_all_time) * 100
            distance_from_atl = ((current_price - atl_all_time) / atl_all_time) * 100
            
            # Calculate all indicators
            data['EMA_20'] = self.calculate_ema(data, 20)
            data['EMA_50'] = self.calculate_ema(data, 50)
            data['EMA_200'] = self.calculate_ema(data, 200)
            data['RSI'] = self.calculate_rsi(data)
            data['MACD'], data['Signal'], data['Histogram'] = self.calculate_macd(data)
            data['ADX'], data['Plus_DI'], data['Minus_DI'] = self.calculate_adx(data)
            data['ATR'] = self.calculate_atr(data)
            data['BB_Upper'], data['BB_Middle'], data['BB_Lower'] = self.calculate_bollinger_bands(data)
            
            # Get latest values
            latest = data.iloc[-1]
            prev = data.iloc[-2]
            
            # Calculate average volume
            avg_volume = data['Volume'].tail(20).mean()
            
            # Skip low volume cryptos
            if avg_volume < 100000:
                return None
            
            # Check for volume divergence (warning sign)
            has_volume_divergence = self.check_volume_divergence(data)
            
            # Find support and resistance levels
            support_level, resistance_level = self.find_support_resistance(data)
            
            # Check weekly trend confirmation
            weekly_bullish = self.check_weekly_trend(ticker)
            
            # Calculate stop loss suggestion (using ATR)
            atr_value = latest['ATR']
            suggested_stop_loss = current_price - (2 * atr_value)  # 2 ATR below current price
            stop_loss_pct = ((current_price - suggested_stop_loss) / current_price) * 100
            
            # Calculate position near support/resistance
            distance_to_support = ((current_price - support_level) / current_price) * 100
            distance_to_resistance = ((resistance_level - current_price) / current_price) * 100
            
            # Risk/Reward ratio
            risk = current_price - suggested_stop_loss
            reward = resistance_level - current_price
            risk_reward_ratio = reward / risk if risk > 0 else 0
            
            # Initialize score
            score = 0
            criteria_met = []
            warnings = []
            
            # Criterion 1: Price above EMAs (25 points)
            if current_price > latest['EMA_20']:
                score += 8
                criteria_met.append("Price > 20 EMA")
            if current_price > latest['EMA_50']:
                score += 8
                criteria_met.append("Price > 50 EMA")
            if current_price > latest['EMA_200']:
                score += 9
                criteria_met.append("Price > 200 EMA")
            
            # Criterion 2: EMAs aligned (10 points)
            if latest['EMA_20'] > latest['EMA_50'] > latest['EMA_200']:
                score += 10
                criteria_met.append("EMAs aligned")
            
            # Criterion 3: RSI in good range (12 points)
            if 40 <= latest['RSI'] <= 70:
                score += 12
                criteria_met.append(f"RSI optimal ({latest['RSI']:.1f})")
            elif 30 <= latest['RSI'] <= 80:
                score += 5
                criteria_met.append(f"RSI acceptable ({latest['RSI']:.1f})")
            
            # Criterion 4: MACD bullish (12 points)
            if latest['MACD'] > latest['Signal']:
                score += 8
                criteria_met.append("MACD bullish")
            if latest['MACD'] > 0:
                score += 4
                criteria_met.append("MACD positive")
            
            # Criterion 5: Volume (8 points)
            if latest['Volume'] > avg_volume:
                score += 8
                criteria_met.append("Volume above average")
            
            # NEW Criterion 6: ADX - Trend Strength (10 points)
            if pd.notna(latest['ADX']) and latest['ADX'] > 25:
                score += 10
                criteria_met.append(f"Strong trend (ADX: {latest['ADX']:.1f})")
            elif pd.notna(latest['ADX']) and latest['ADX'] > 20:
                score += 5
                criteria_met.append(f"Moderate trend (ADX: {latest['ADX']:.1f})")
            
            # NEW Criterion 7: Weekly trend confirmation (10 points)
            if weekly_bullish:
                score += 10
                criteria_met.append("Weekly trend confirmed")
            
            # NEW Criterion 8: Bollinger Band position (5 points)
            if latest['Close'] > latest['BB_Middle']:
                score += 5
                criteria_met.append("Above BB middle")
            
            # NEW Criterion 9: Good risk/reward ratio (8 points)
            if risk_reward_ratio > 2:
                score += 8
                criteria_met.append(f"R:R {risk_reward_ratio:.1f}:1")
            elif risk_reward_ratio > 1.5:
                score += 4
                criteria_met.append(f"R:R {risk_reward_ratio:.1f}:1")
            
            # WARNING FLAGS (reduce score)
            if has_volume_divergence:
                score -= 10
                warnings.append("⚠ Volume divergence detected")
            
            if pd.notna(latest['RSI']) and latest['RSI'] > 75:
                score -= 5
                warnings.append("⚠ Overbought RSI")
            
            # Filter out recent pumps (>40% in 24h from CMC data)
            cmc_24h = self.get_cmc_info(ticker).get('percent_change_24h', 0)
            if cmc_24h > 40:
                score -= 15
                warnings.append("⚠ Recent pump detected")
            
            # Only return cryptos with score >= 40 (adjusted for bear market)
            if score < 40:
                return None
            
            # Calculate additional metrics
            month_ago_price = data['Close'].iloc[-20] if len(data) >= 20 else data['Close'].iloc[0]
            month_change = ((current_price - month_ago_price) / month_ago_price) * 100
            week_ago_price = data['Close'].iloc[-5]
            week_change = ((current_price - week_ago_price) / week_ago_price) * 100
            
            # Distance from all-time high in period
            high_period = data['Close'].max()
            distance_from_high = ((current_price - high_period) / high_period) * 100
            
            return {
                'ticker': ticker,
                'score': score,
                'price': current_price,
                'rsi': latest['RSI'],
                'macd': latest['MACD'],
                'signal': latest['Signal'],
                'volume': latest['Volume'],
                'avg_volume': avg_volume,
                'week_change': week_change,
                'month_change': month_change,
                'distance_from_high': distance_from_high,
                'ema_20': latest['EMA_20'],
                'ema_50': latest['EMA_50'],
                'ema_200': latest['EMA_200'],
                'criteria_met': criteria_met,
                # NEW enhanced metrics
                'adx': latest['ADX'],
                'atr': atr_value,
                'support': support_level,
                'resistance': resistance_level,
                'stop_loss': suggested_stop_loss,
                'stop_loss_pct': stop_loss_pct,
                'risk_reward': risk_reward_ratio,
                'distance_to_support': distance_to_support,
                'distance_to_resistance': distance_to_resistance,
                'weekly_bullish': weekly_bullish,
                'volume_divergence': has_volume_divergence,
                'warnings': warnings,
                # CoinMarketCap data
                'cmc_name': self.get_cmc_info(ticker).get('name', ''),
                'market_cap': self.get_cmc_info(ticker).get('market_cap', 0),
                'market_cap_rank': self.get_cmc_info(ticker).get('market_cap_rank', 0),
                'cmc_24h_change': self.get_cmc_info(ticker).get('percent_change_24h', 0),
                'cmc_7d_change': self.get_cmc_info(ticker).get('percent_change_7d', 0),
                'cmc_30d_change': self.get_cmc_info(ticker).get('percent_change_30d', 0),
                # Sector classification
                'sector': self.get_crypto_sector(ticker),
                # ATH/ATL data
                'ath': ath_all_time,
                'atl': atl_all_time,
                'distance_from_ath': distance_from_ath,
                'distance_from_atl': distance_from_atl
            }
            
        except Exception as e:
            # Silently skip stocks with errors
            return None
    
    def scan(self, min_score=60, max_results=50):
        """
        Scan all cryptos and return those meeting criteria
        
        Args:
            min_score: Minimum score to include (0-100)
            max_results: Maximum number of results to return
            
        Returns:
            DataFrame with scan results
        """
        print(f"Scanning {len(self.crypto_list)} cryptocurrencies...")
        print("This may take several minutes...\n")
        
        results = []
        processed = 0
        
        for ticker in self.crypto_list:
            processed += 1
            if processed % 10 == 0:  # Report every 10 for smaller list
                print(f"Processed {processed}/{len(self.crypto_list)} cryptos...")
            
            result = self.check_uptrend_criteria(ticker)
            if result and result['score'] >= min_score:
                results.append(result)
            
            # Add small delay to avoid Yahoo Finance rate limiting
            time.sleep(0.5)  # 500ms delay between requests
        
        print(f"\nScan complete! Found {len(results)} cryptos meeting criteria.\n")
        
        if not results:
            return pd.DataFrame()
        
        # Convert to DataFrame and sort by score
        df = pd.DataFrame(results)
        df = df.sort_values('score', ascending=False).head(max_results)
        
        return df
    
    def print_results(self, df, detailed=False):
        """
        Print scan results in a readable format
        
        Args:
            df: DataFrame with scan results
            detailed: If True, show detailed criteria for each crypto
        """
        if df.empty:
            print("No cryptocurrencies found meeting the criteria.")
            print("Try lowering the min_score or expanding your crypto list.")
            return
        
        print("=" * 100)
        print(f"{'CRYPTO TREND SCANNER RESULTS':.^100}")
        print(f"{'Scan Date: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):.^100}")
        print("=" * 100)
        print()
        
        # Summary table
        print(f"{'Crypto':<12} {'Score':<7} {'Price':<15} {'RSI':<7} {'Week %':<9} {'Month %':<9} {'From High':<10}")
        print("-" * 100)
        
        for _, row in df.iterrows():
            # Format price based on value
            if row['price'] >= 1:
                price_str = f"${row['price']:,.2f}"
            elif row['price'] >= 0.01:
                price_str = f"${row['price']:.4f}"
            else:
                price_str = f"${row['price']:.6f}"
            
            print(f"{row['ticker']:<12} "
                  f"{row['score']:<7.0f} "
                  f"{price_str:<15} "
                  f"{row['rsi']:<7.1f} "
                  f"{row['week_change']:>8.1f}% "
                  f"{row['month_change']:>8.1f}% "
                  f"{row['distance_from_high']:>9.1f}%")
        
        print()
        
        # Detailed view if requested
        if detailed:
            print("\n" + "=" * 100)
            print("DETAILED ANALYSIS")
            print("=" * 100)
            
            for _, row in df.iterrows():
                print(f"\n{row['ticker']} - Score: {row['score']:.0f}/100")
                print(f"  Price: ${row['price']:.2f}")
                print(f"  RSI: {row['rsi']:.1f}")
                print(f"  MACD: {row['macd']:.2f} (Signal: {row['signal']:.2f})")
                print(f"  Volume: {row['volume']:,.0f} (Avg: {row['avg_volume']:,.0f})")
                print(f"  EMAs: 20={row['ema_20']:.2f}, 50={row['ema_50']:.2f}, 200={row['ema_200']:.2f}")
                print(f"  Performance: Week {row['week_change']:+.1f}%, Month {row['month_change']:+.1f}%")
                print(f"  Distance from Period High: {row['distance_from_high']:.1f}%")
                print(f"  Criteria Met:")
                for criterion in row['criteria_met']:
                    print(f"    ✓ {criterion}")
        
        print("\n" + "=" * 100)
        print("NEXT STEPS:")
        print("1. Review charts for these cryptos on TradingView or your exchange")
        print("2. Look for clean price action and clear support/resistance")
        print("3. Wait for proper entry signals (pullbacks, breakouts)")
        print("4. Set stop losses and position sizes before entering")
        print("5. Never risk more than 1-2% of your portfolio per trade")
        print("6. Remember: Crypto is 24/7 and highly volatile - manage risk carefully")
        print("=" * 100)
    
    def export_to_csv(self, df, filename=None):
        """
        Export results to CSV file
        
        Args:
            df: DataFrame with scan results
            filename: Output filename (default: scan_results_YYYYMMDD.csv)
        """
        if df.empty:
            print("No results to export.")
            return
        
        if filename is None:
            filename = f"scan_results_{datetime.now().strftime('%Y%m%d')}.csv"
        
        # Select columns for export
        export_df = df[['ticker', 'score', 'price', 'rsi', 'macd', 'signal', 
                       'week_change', 'month_change', 'distance_from_high',
                       'volume', 'avg_volume']]
        
        export_df.to_csv(filename, index=False)
        print(f"\nResults exported to: {filename}")


def main():
    """
    Main function to run the scanner
    """
    print("\n" + "=" * 100)
    print(f"{'CRYPTO TREND SCANNER':.^100}")
    print("=" * 100)
    print("\nThis scanner identifies cryptocurrencies in strong uptrends.")
    print("Data sources: CoinMarketCap (top 500 rankings) + Yahoo Finance (price/indicators)\n")
    
    # Option 1: Scan top 500 from CoinMarketCap (default)
    scanner = CryptoScanner(use_cmc=True)
    
    # Option 2: Scan custom list (uncomment and modify)
    # custom_cryptos = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'MATIC-USD', 'AVAX-USD']
    # scanner = CryptoScanner(crypto_list=custom_cryptos)
    
    # Run the scan
    results = scanner.scan(min_score=60, max_results=30)
    
    # Print results
    scanner.print_results(results, detailed=True)
    
    # Export to CSV
    if not results.empty:
        scanner.export_to_csv(results)
    
    print("\nScan complete!")


if __name__ == "__main__":
    main()