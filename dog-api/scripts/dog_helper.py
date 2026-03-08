#!/usr/bin/env python3
import sys
import requests
import json
import argparse

BASE_URL = "https://dog.ceo/api"

def get_random_image():
    url = f"{BASE_URL}/breeds/image/random"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def list_breeds():
    url = f"{BASE_URL}/breeds/list/all"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def get_images_by_breed(breed, sub_breed=None):
    if sub_breed:
        url = f"{BASE_URL}/breed/{breed}/{sub_breed}/images/random"
    else:
        url = f"{BASE_URL}/breed/{breed}/images/random"
    
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def main():
    parser = argparse.ArgumentParser(description='Dog API Helper - All about dogs')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Random Image
    subparsers.add_parser('random', help='Get a random dog image')

    # List Breeds
    subparsers.add_parser('list', help='List all dog breeds')

    # Images by Breed
    breed_parser = subparsers.add_parser('breed', help='Get a random image of a specific breed')
    breed_parser.add_argument('breed', type=str, help='Dog breed name')
    breed_parser.add_argument('--sub', type=str, help='Sub-breed name (optional)')

    args = parser.parse_args()

    try:
        if args.command == 'random':
            result = get_random_image()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'list':
            result = list_breeds()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == 'breed':
            result = get_images_by_breed(args.breed, args.sub)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
