#!/usr/bin/env python3
"""
Quick start script for Crypto Scanner
"""

from stock_scanner import CryptoScanner

def main():
    print("\n" + "=" * 100)
    print(f"{'CRYPTO TREND SCANNER':.^100}")
    print("=" * 100)
    print("\nScanning top cryptocurrencies for uptrends...\n")
    
    # Create scanner with top cryptos
    scanner = CryptoScanner()
    
    # Run the scan (min_score=60 means moderate to strong uptrends)
    results = scanner.scan(min_score=60, max_results=30)
    
    # Print detailed results
    scanner.print_results(results, detailed=True)
    
    # Export to CSV
    if not results.empty:
        scanner.export_to_csv(results, "crypto_scan_results.csv")
    
    print("\n✅ Scan complete!")

if __name__ == "__main__":
    main()
