#!/usr/bin/env python3
import sys
import requests
import json
import argparse

def get_joke(category='Any', joke_type=None, blacklist=None, safe_mode=True):
    url = f"https://v2.jokeapi.dev/joke/{category}"
    params = {}
    
    if joke_type:
        params['type'] = joke_type
    if blacklist:
        params['blacklistFlags'] = blacklist
    if safe_mode:
        params['safe-mode'] = ''

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('error'):
            raise Exception(data.get('additionalInfo', 'Unknown error from JokeAPI'))
            
        return data
    except Exception as e:
        raise Exception(f"Failed to fetch joke: {e}")

def format_joke(data):
    if data['type'] == 'single':
        return data['joke']
    else:
        return f"{data['setup']}\n\n... {data['delivery']}"

def main():
    parser = argparse.ArgumentParser(description='JokeAPI Helper - Fetch random jokes')
    parser.add_argument('--category', type=str, default='Any', help='Joke category (Programming, Misc, Dark, Pun, Spooky, Christmas, Any)')
    parser.add_argument('--type', type=str, choices=['single', 'twopart'], help='Joke type')
    parser.add_argument('--blacklist', type=str, help='Comma-separated flags to blacklist (nsfw, religious, political, racist, sexist, explicit)')
    parser.add_argument('--unsafe', action='store_false', dest='safe_mode', help='Disable safe mode')
    parser.add_argument('--raw', action='store_true', help='Output raw JSON')

    args = parser.parse_args()

    try:
        joke_data = get_joke(args.category, args.type, args.blacklist, args.safe_mode)
        
        if args.raw:
            print(json.dumps(joke_data, indent=2, ensure_ascii=False))
        else:
            print(f"[{joke_data['category']}]")
            print("-" * 20)
            print(format_joke(joke_data))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
