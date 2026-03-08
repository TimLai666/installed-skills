#!/usr/bin/env python3
import sys
import requests
import json
import argparse

def get_exchange_rate(base, target):
    base = base.lower()
    target = target.lower()
    
    # Try different CDN endpoints for reliability
    endpoints = [
        f"https://latest.currency-api.pages.dev/v1/currencies/{base}.json",
        f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"
    ]
    
    last_error = None
    for url in endpoints:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if base in data and target in data[base]:
                return data[base][target], data['date']
            elif target in data: # Some endpoints might have different structures
                return data[target], data['date']
        except Exception as e:
            last_error = e
            continue
            
    raise Exception(f"Failed to fetch exchange rate for {base} to {target}. Last error: {last_error}")

def main():
    parser = argparse.ArgumentParser(description='Currency Converter using fawazahmed0/currency-api')
    parser.add_argument('--base', type=str, default='twd', help='Base currency (default: twd)')
    parser.add_argument('--target', type=str, required=True, help='Target currency')
    parser.add_argument('--amount', type=float, default=1.0, help='Amount to convert')
    parser.add_argument('--list', action='store_true', help='List all supported currencies')

    args = parser.parse_args()

    if args.list:
        url = "https://latest.currency-api.pages.dev/v1/currencies.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            print(json.dumps(response.json(), indent=2))
        except Exception as e:
            print(f"Error fetching currency list: {e}")
            sys.exit(1)
        return

    try:
        rate, date = get_exchange_rate(args.base, args.target)
        result = args.amount * rate
        output = {
            "base": args.base.upper(),
            "target": args.target.upper(),
            "amount": args.amount,
            "rate": rate,
            "result": result,
            "date": date,
            "source": "fawazahmed0/currency-api"
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
