#!/usr/bin/env python3
"""
Flask Web Application for Crypto Scanner
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from stock_scanner import CryptoScanner
import pandas as pd
from datetime import datetime
import json
import numpy as np

app = Flask(__name__)

# Enable CORS for all routes (allows website to call this API)
CORS(app)

# Global variable to store scan results
last_scan_results = None
scan_status = {"status": "idle", "progress": 0, "message": ""}
market_context = {}  # Store market-wide data

@app.route('/api/indicators/<symbol>')
def get_indicators(symbol):
    """
    Quick technical indicators for OmegaZoid chat widget
    Returns: RSI, ADX, price, trend analysis
    
    Example: /api/indicators/BTC
    """
    try:
        # Simple response for testing
        if symbol.upper() == 'TEST':
            return jsonify({
                'success': True,
                'symbol': 'TEST',
                'message': 'Scanner API is working!',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Create scanner
        print(f"Creating scanner for {symbol}...")
        scanner = CryptoScanner(use_cmc=False)
        ticker = f"{symbol.upper()}-USD"
        
        print(f"Analyzing {ticker}...")
        # Get analysis
        result = scanner.check_uptrend_criteria(ticker)
        
        if result:
            print(f"Got result for {ticker}")
            # Safely extract values with defaults
            adx_value = float(result.get('adx', 0))
            rsi_value = float(result.get('rsi', 50))
            price_value = float(result.get('price', 0))
            support_value = float(result.get('support', 0))
            resistance_value = float(result.get('resistance', 0))
            
            # Replace NaN/Inf with safe defaults
            import math
            if math.isnan(adx_value) or math.isinf(adx_value):
                adx_value = 0
            if math.isnan(rsi_value) or math.isinf(rsi_value):
                rsi_value = 50
            if math.isnan(price_value) or math.isinf(price_value):
                price_value = 0
            if math.isnan(support_value) or math.isinf(support_value):
                support_value = 0
            if math.isnan(resistance_value) or math.isinf(resistance_value):
                resistance_value = 0
            
            # Calculate trend strength from ADX
            if adx_value > 50:
                trend_strength = 'Strong'
            elif adx_value > 25:
                trend_strength = 'Moderate'
            else:
                trend_strength = 'Weak'
            
            # Determine RSI signal
            if rsi_value < 30:
                rsi_signal = 'Oversold'
            elif rsi_value > 70:
                rsi_signal = 'Overbought'
            else:
                rsi_signal = 'Neutral'
            
            return jsonify({
                'success': True,
                'symbol': symbol.upper(),
                'price': round(price_value, 8 if price_value < 1 else 4),
                'rsi': round(rsi_value, 2),
                'rsi_signal': rsi_signal,
                'adx': round(adx_value, 2),
                'trend_strength': trend_strength,
                'price_change_24h': round(float(result.get('cmc_24h_change', 0)), 2),
                'market_cap': float(result.get('market_cap', 0)),
                'volume_24h': float(result.get('volume', 0)),
                'support': round(support_value, 8 if support_value < 1 else 4),
                'resistance': round(resistance_value, 8 if resistance_value < 1 else 4),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            print(f"No result for {ticker}")
            return jsonify({
                'success': False,
                'error': f'Unable to fetch data for {symbol.upper()}. Token may not be available in Yahoo Finance. Try BTC, ETH, SOL, etc.'
            }), 404
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR in get_indicators: {error_trace}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}',
            'type': type(e).__name__
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'OmegaZoid Scanner API',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/market-context')
def get_market_context():
    """Get market-wide context data"""
    global market_context
    
    try:
        scanner = CryptoScanner(use_cmc=False)
        
        # Get Fear & Greed Index
        fear_greed = scanner.get_fear_greed_index()
        
        # Get Bitcoin Dominance
        dominance = scanner.get_bitcoin_dominance()
        
        market_context = {
            'fear_greed': fear_greed,
            'dominance': dominance,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify({
            'success': True,
            'data': market_context
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/scan', methods=['POST'])
def scan():
    """Run the crypto scan"""
    global last_scan_results, scan_status
    
    try:
        # Get parameters from request
        data = request.json
        min_score = int(data.get('min_score', 60))
        max_results = int(data.get('max_results', 50))
        preset = data.get('preset', 'all')
        kraken_only = data.get('kraken_only', False)
        cryptocom_only = data.get('cryptocom_only', False)
        
        scan_status = {"status": "running", "progress": 0, "message": "Initializing scan..."}
        
        # Create scanner with exchange filter if requested
        scanner = CryptoScanner(use_cmc=True)
        if kraken_only:
            # Re-initialize with Kraken filter
            scanner = CryptoScanner(crypto_list=None, use_cmc=True)
            scanner.crypto_list = scanner.get_top_cryptos_from_cmc(limit=250, filter_kraken=True)
        elif cryptocom_only:
            # Re-initialize with Crypto.com filter
            scanner = CryptoScanner(crypto_list=None, use_cmc=True)
            scanner.crypto_list = scanner.get_top_cryptos_from_cmc(limit=250, filter_cryptocom=True)
        
        # Run scan
        scan_status["message"] = f"Scanning {len(scanner.crypto_list)} cryptocurrencies..."
        results = scanner.scan(min_score=min_score, max_results=max_results)
        
        # Apply preset filters if specified
        if preset != 'all' and not results.empty:
            results = apply_preset_filter(results, preset)
        
        scan_status = {"status": "complete", "progress": 100, "message": "Scan complete!"}
        
        if results.empty:
            return jsonify({
                'success': True,
                'count': 0,
                'data': [],
                'message': 'No cryptocurrencies found meeting the criteria. Try lowering the minimum score.'
            })
        
        # Convert to JSON-friendly format
        results_list = results.to_dict('records')
        
        # Format the data
        for item in results_list:
            item['criteria_met'] = ', '.join(item['criteria_met'])
            item['warnings'] = item.get('warnings', [])
            item['price'] = round(item['price'], 8)
            item['rsi'] = round(item['rsi'], 2)
            item['macd'] = round(item['macd'], 4)
            item['signal'] = round(item['signal'], 4)
            item['week_change'] = round(item['week_change'], 2)
            item['month_change'] = round(item['month_change'], 2)
            item['distance_from_high'] = round(item['distance_from_high'], 2)
            # Format CMC data
            item['market_cap'] = item.get('market_cap', 0)
            item['cmc_24h_change'] = round(item.get('cmc_24h_change', 0), 2)
            item['cmc_7d_change'] = round(item.get('cmc_7d_change', 0), 2)
            item['cmc_30d_change'] = round(item.get('cmc_30d_change', 0), 2)
            # Format new enhanced data
            item['adx'] = round(item.get('adx', 0), 2)
            item['atr'] = round(item.get('atr', 0), 6)
            item['support'] = round(item.get('support', 0), 8)
            item['resistance'] = round(item.get('resistance', 0), 8)
            item['stop_loss'] = round(item.get('stop_loss', 0), 8)
            item['stop_loss_pct'] = round(item.get('stop_loss_pct', 0), 2)
            item['risk_reward'] = round(item.get('risk_reward', 0), 2)
            item['distance_to_support'] = round(item.get('distance_to_support', 0), 2)
            item['distance_to_resistance'] = round(item.get('distance_to_resistance', 0), 2)
            item['weekly_bullish'] = item.get('weekly_bullish', False)
            item['volume_divergence'] = item.get('volume_divergence', False)
            # Add sector
            item['sector'] = item.get('sector', 'Other')
            # Format ATH/ATL data
            item['ath'] = round(item.get('ath', 0), 8) if item.get('ath', 0) < 1 else round(item.get('ath', 0), 2)
            item['atl'] = round(item.get('atl', 0), 8) if item.get('atl', 0) < 1 else round(item.get('atl', 0), 2)
            item['distance_from_ath'] = round(item.get('distance_from_ath', 0), 2)
            item['distance_from_atl'] = round(item.get('distance_from_atl', 0), 2)
        
        last_scan_results = results
        
        return jsonify({
            'success': True,
            'count': len(results_list),
            'data': results_list,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        scan_status = {"status": "error", "progress": 0, "message": str(e)}
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/status')
def status():
    """Get scan status"""
    return jsonify(scan_status)

@app.route('/export/csv')
def export_csv():
    """Export results to CSV"""
    global last_scan_results
    
    if last_scan_results is None or last_scan_results.empty:
        return jsonify({'success': False, 'error': 'No scan results available'}), 400
    
    filename = f"crypto_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    scanner = CryptoScanner()
    scanner.export_to_csv(last_scan_results, filename)
    
    return jsonify({'success': True, 'filename': filename})

@app.route('/calculate-position', methods=['POST'])
def calculate_position():
    """Calculate position size and P/L"""
    try:
        data = request.json
        account_size = float(data.get('account_size', 10000))
        risk_percent = float(data.get('risk_percent', 1))
        entry_price = float(data.get('entry_price'))
        stop_loss = float(data.get('stop_loss'))
        target_price = float(data.get('target_price'))
        
        scanner = CryptoScanner(use_cmc=False)
        
        # Calculate position size
        position = scanner.calculate_position_size(
            account_size, risk_percent, entry_price, stop_loss
        )
        
        # Calculate P/L
        pl = scanner.calculate_profit_loss(
            entry_price, target_price, stop_loss, position['value_usd']
        )
        
        return jsonify({
            'success': True,
            'position': position,
            'profit_loss': pl
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/correlation-analysis')
def correlation_analysis():
    """Analyze correlation between selected cryptos"""
    global last_scan_results
    
    try:
        if last_scan_results is None or last_scan_results.empty:
            return jsonify({'success': False, 'error': 'No scan results available'}), 400
        
        import yfinance as yf
        
        # Get top 10 cryptos from results
        top_cryptos = last_scan_results.head(10)['ticker'].tolist()
        
        # Download recent price data
        data = yf.download(top_cryptos, period='1mo', progress=False)['Close']
        
        # Calculate correlation matrix
        if isinstance(data, pd.Series):
            # Only one crypto
            correlation_matrix = [[1.0]]
            tickers = [top_cryptos[0]]
        else:
            correlation_matrix = data.corr().round(2).values.tolist()
            tickers = data.columns.tolist()
        
        return jsonify({
            'success': True,
            'tickers': tickers,
            'correlation_matrix': correlation_matrix
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def apply_preset_filter(results, preset):
    """Apply preset filters to results"""
    if preset == 'aggressive':
        return results[
            (results['rsi'] > 60) &
            (results['week_change'] > 10) &
            (results['distance_from_high'] > -15)
        ]
    elif preset == 'conservative':
        return results[
            (results['rsi'] >= 50) & (results['rsi'] <= 65) &
            (results['month_change'] > 0)
        ]
    elif preset == 'pullback':
        return results[
            (results['rsi'] >= 40) & (results['rsi'] <= 55) &
            (results['week_change'] < 5) &
            (results['month_change'] > 10)
        ]
    elif preset == 'breakout':
        return results[
            (results['rsi'] >= 55) & (results['rsi'] <= 70) &
            (results['distance_from_high'] > -10) &
            (results['volume'] > results['avg_volume'] * 1.2)
        ]
    elif preset == 'largecap':
        large_caps = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD', 
                      'DOGE-USD', 'SOL-USD', 'TRX-USD', 'DOT-USD', 'MATIC-USD']
        return results[results['ticker'].isin(large_caps)]
    else:
        return results

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("CRYPTO SCANNER WEB APPLICATION".center(80))
    print("=" * 80)
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
