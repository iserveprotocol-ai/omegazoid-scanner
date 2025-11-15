#!/usr/bin/env python3
"""
Crypto Scanner Presets
Pre-configured scanner settings for different crypto trading styles
"""

from stock_scanner import CryptoScanner
import pandas as pd

class CryptoScannerPresets:
    """
    Pre-configured scanner settings for different crypto trading strategies
    """
    
    @staticmethod
    def aggressive_growth():
        """
        Aggressive Growth Scanner
        - High momentum cryptos
        - Higher risk, higher reward
        - Best for experienced traders
        """
        print("\n🚀 AGGRESSIVE GROWTH SCANNER")
        print("=" * 80)
        print("Target: High momentum cryptos with strong uptrends")
        print("Risk Level: HIGH")
        print("Time Frame: Short to medium term")
        print("=" * 80 + "\n")
        
        # Scan with lower minimum score to catch more aggressive movers
        scanner = CryptoScanner()
        results = scanner.scan(min_score=70, max_results=20)
        
        # Filter for high momentum
        if not results.empty:
            results = results[
                (results['rsi'] > 60) &  # Strong momentum
                (results['week_change'] > 10) &  # Strong weekly gain (crypto moves more)
                (results['distance_from_high'] > -15)  # Near highs
            ]
        
        return results
    
    @staticmethod
    def conservative_quality():
        """
        Conservative Quality Scanner
        - Established uptrends
        - Lower risk (for crypto)
        - Best for beginners
        """
        print("\n🛡️ CONSERVATIVE QUALITY SCANNER")
        print("=" * 80)
        print("Target: Stable, established uptrends")
        print("Risk Level: LOW-MEDIUM (still crypto!)")
        print("Time Frame: Medium to long term")
        print("=" * 80 + "\n")
        
        scanner = CryptoScanner()
        results = scanner.scan(min_score=80, max_results=15)
        
        # Filter for quality (focus on major cryptos)
        if not results.empty:
            results = results[
                (results['rsi'] >= 50) & (results['rsi'] <= 65) &  # Healthy momentum
                (results['month_change'] > 0)  # Positive monthly trend
            ]
        
        return results
    
    @staticmethod
    def pullback_entry():
        """
        Pullback Entry Scanner
        - Cryptos pulling back in uptrends
        - Best entry points
        - Good risk-reward
        """
        print("\n📉 PULLBACK ENTRY SCANNER")
        print("=" * 80)
        print("Target: Uptrending cryptos pulling back to support")
        print("Risk Level: MEDIUM")
        print("Time Frame: Short to medium term")
        print("=" * 80 + "\n")
        
        scanner = CryptoScanner()
        results = scanner.scan(min_score=65, max_results=20)
        
        # Filter for pullbacks
        if not results.empty:
            results = results[
                (results['rsi'] >= 40) & (results['rsi'] <= 55) &  # RSI reset
                (results['week_change'] < 5) &  # Not running away
                (results['month_change'] > 10)  # But strong monthly trend
            ]
        
        return results
    
    @staticmethod
    def breakout_candidates():
        """
        Breakout Candidates Scanner
        - Cryptos near resistance
        - Potential breakouts
        - High volume confirmation needed
        """
        print("\n💥 BREAKOUT CANDIDATES SCANNER")
        print("=" * 80)
        print("Target: Cryptos consolidating near resistance")
        print("Risk Level: MEDIUM-HIGH")
        print("Time Frame: Short term")
        print("=" * 80 + "\n")
        
        scanner = CryptoScanner()
        results = scanner.scan(min_score=70, max_results=20)
        
        # Filter for breakout potential
        if not results.empty:
            results = results[
                (results['rsi'] >= 55) & (results['rsi'] <= 70) &  # Building momentum
                (results['distance_from_high'] > -10) &  # Near highs
                (results['volume'] > results['avg_volume'] * 1.2)  # Above average volume
            ]
        
        return results
    
    @staticmethod
    def swing_trading():
        """
        Swing Trading Scanner
        - 3-10 day holds
        - Balanced risk-reward
        - Most popular style
        """
        print("\n🎯 SWING TRADING SCANNER")
        print("=" * 80)
        print("Target: Multi-day swing opportunities")
        print("Risk Level: MEDIUM")
        print("Time Frame: 3-10 days")
        print("=" * 80 + "\n")
        
        scanner = CryptoScanner()
        results = scanner.scan(min_score=70, max_results=20)
        
        # Filter for swing setups
        if not results.empty:
            results = results[
                (results['rsi'] >= 45) & (results['rsi'] <= 65) &  # Good range
                (results['week_change'] > 0)  # Positive momentum
            ]
        
        return results
    
    @staticmethod
    def position_trading():
        """
        Position Trading Scanner
        - Weeks to months holds
        - Strong long-term trends
        - Lowest time commitment
        """
        print("\n📊 POSITION TRADING SCANNER")
        print("=" * 80)
        print("Target: Long-term trend opportunities")
        print("Risk Level: LOW-MEDIUM")
        print("Time Frame: Weeks to months")
        print("=" * 80 + "\n")
        
        scanner = CryptoScanner()
        results = scanner.scan(min_score=75, max_results=15)
        
        # Filter for position trades
        if not results.empty:
            results = results[
                (results['month_change'] > 15) &  # Strong monthly trend (adjusted for crypto)
                (results['rsi'] >= 50)  # Bullish momentum
            ]
        
        return results
    
    @staticmethod
    def large_cap_cryptos():
        """
        Large Cap Crypto Scanner
        - Major cryptocurrencies only
        - Lower volatility (relatively)
        - Better liquidity
        """
        print("\n💎 LARGE CAP CRYPTO SCANNER")
        print("=" * 80)
        print("Target: Major cryptocurrencies in uptrends")
        print("Market Cap: Large cap only")
        print("=" * 80 + "\n")
        
        large_cap_cryptos = [
            'BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD', 
            'DOGE-USD', 'SOL-USD', 'TRX-USD', 'DOT-USD', 'MATIC-USD',
            'LTC-USD', 'AVAX-USD', 'LINK-USD', 'UNI-USD', 'ATOM-USD'
        ]
        
        scanner = CryptoScanner(crypto_list=large_cap_cryptos)
        results = scanner.scan(min_score=65, max_results=10)
        
        return results
    
    @staticmethod
    def defi_tokens():
        """
        DeFi Tokens Scanner
        - DeFi ecosystem tokens
        - Higher risk, higher reward
        - For experienced traders
        """
        print("\n🌐 DEFI TOKENS SCANNER")
        print("=" * 80)
        print("Target: DeFi tokens with strong momentum")
        print("Risk Level: HIGH")
        print("Note: Higher volatility, use smaller position sizes")
        print("=" * 80 + "\n")
        
        defi_tokens = [
            'UNI-USD', 'LINK-USD', 'AAVE-USD', 'CRV-USD', 'SUSHI-USD',
            'COMP-USD', 'SNX-USD', 'CAKE-USD', 'LRC-USD', 'GRT-USD'
        ]
        
        scanner = CryptoScanner(crypto_list=defi_tokens)
        results = scanner.scan(min_score=70, max_results=10)
        
        # Filter for momentum
        if not results.empty:
            results = results[
                (results['week_change'] > 5)  # Strong momentum
            ]
        
        return results


def run_preset(preset_name):
    """
    Run a specific preset scanner
    
    Args:
        preset_name: Name of the preset to run
    """
    presets = {
        'aggressive': CryptoScannerPresets.aggressive_growth,
        'conservative': CryptoScannerPresets.conservative_quality,
        'pullback': CryptoScannerPresets.pullback_entry,
        'breakout': CryptoScannerPresets.breakout_candidates,
        'swing': CryptoScannerPresets.swing_trading,
        'position': CryptoScannerPresets.position_trading,
        'largecap': CryptoScannerPresets.large_cap_cryptos,
        'defi': CryptoScannerPresets.defi_tokens
    }
    
    if preset_name.lower() in presets:
        results = presets[preset_name.lower()]()
        
        if not results.empty:
            scanner = CryptoScanner()
            scanner.print_results(results, detailed=True)
            scanner.export_to_csv(results, f"{preset_name}_scan_results.csv")
        else:
            print("\n❌ No cryptos found meeting the criteria.")
            print("Try adjusting the filters or scanning at a different time.")
    else:
        print(f"\n❌ Preset '{preset_name}' not found.")
        print("\nAvailable presets:")
        print("  - aggressive: High momentum, high risk")
        print("  - conservative: Stable trends, lower risk")
        print("  - pullback: Pullback entries in uptrends")
        print("  - breakout: Breakout candidates")
        print("  - swing: Swing trading opportunities")
        print("  - position: Long-term position trades")
        print("  - largecap: Large cap cryptos only")
        print("  - defi: DeFi tokens")


def main():
    """
    Interactive menu for preset scanners
    """
    print("\n" + "=" * 80)
    print("CRYPTO SCANNER PRESETS".center(80))
    print("=" * 80)
    print("\nChoose a scanning strategy:\n")
    print("1. Aggressive Growth (High risk, high reward)")
    print("2. Conservative Quality (Lower risk, major cryptos)")
    print("3. Pullback Entry (Best entry points)")
    print("4. Breakout Candidates (Momentum plays)")
    print("5. Swing Trading (3-10 day holds)")
    print("6. Position Trading (Weeks to months)")
    print("7. Large Cap Cryptos (Major cryptos only)")
    print("8. DeFi Tokens (DeFi ecosystem)")
    print("\n0. Exit")
    print("\n" + "=" * 80)
    
    choice = input("\nEnter your choice (0-8): ").strip()
    
    presets = {
        '1': 'aggressive',
        '2': 'conservative',
        '3': 'pullback',
        '4': 'breakout',
        '5': 'swing',
        '6': 'position',
        '7': 'largecap',
        '8': 'defi'
    }
    
    if choice == '0':
        print("\nGoodbye!")
        return
    elif choice in presets:
        run_preset(presets[choice])
    else:
        print("\n❌ Invalid choice. Please run again and select 0-8.")


if __name__ == "__main__":
    main()