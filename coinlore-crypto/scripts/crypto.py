#!/usr/bin/env python3
import sys
import requests
import json
import argparse

# CoinLore API Base URL
BASE_URL = "https://api.coinlore.net/api"

def get_coin_by_id(coin_id):
    url = f"{BASE_URL}/ticker/?id={coin_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data[0] if data else None

def search_coin_by_symbol(symbol):
    symbol = symbol.upper()
    # Fetch first 100 coins to find the symbol (standard lookup)
    # For a more robust solution, we'd fetch the full list, but top 100 covers most common requests
    url = f"{BASE_URL}/tickers/?start=0&limit=100"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    for coin in data.get('data', []):
        if coin['symbol'] == symbol:
            return coin
    return None

def get_global_stats():
    url = f"{BASE_URL}/global/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()[0]

def main():
    parser = argparse.ArgumentParser(description='CoinLore Crypto Market Data')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Get by ID
    get_parser = subparsers.add_parser('get', help='Get coin data by ID')
    get_parser.add_argument('id', type=str, help='Coin ID (e.g., 90 for BTC)')

    # Search by Symbol
    search_parser = subparsers.add_parser('search', help='Search coin by symbol')
    search_parser.add_argument('symbol', type=str, help='Currency symbol (e.g., BTC, ETH)')

    # Global Stats
    subparsers.add_parser('global', help='Get global market stats')

    args = parser.parse_args()

    try:
        if args.command == 'get':
            result = get_coin_by_id(args.id)
            if result:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Error: Coin with ID {args.id} not found.")
                sys.exit(1)
        
        elif args.command == 'search':
            result = search_coin_by_symbol(args.symbol)
            if result:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                # If not in top 100, try a broader search or notify
                print(f"Error: Symbol {args.symbol} not found in top 100. Try providing the exact ID if known.")
                sys.exit(1)

        elif args.command == 'global':
            result = get_global_stats()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
