#!/usr/bin/env python3
import sys
import requests
import json
import argparse

BASE_URL = "https://gutendex.com/books/"

def search_books(query=None, author=None, topic=None):
    params = {}
    if query:
        params['search'] = query
    if author:
        params['author'] = author # Though search covers this, specific filters might exist
    if topic:
        params['topic'] = topic

    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()
    return response.json()

def main():
    parser = argparse.ArgumentParser(description='Gutendex Book Search Helper')
    parser.add_argument('query', type=str, nargs='?', help='Search query (title or author)')
    parser.add_argument('--topic', type=str, help='Filter by topic/subject')
    parser.add_argument('--raw', action='store_true', help='Output raw JSON')

    args = parser.parse_args()

    if not args.query and not args.topic:
        parser.print_help()
        sys.exit(0)

    try:
        data = search_books(query=args.query, topic=args.topic)
        
        if args.raw:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            results = data.get('results', [])
            print(f"Found {data.get('count', 0)} books matching your search.\n")
            for book in results[:10]: # Limit to top 10 for terminal output
                authors = ", ".join([a['name'] for a in book['authors']])
                print(f"ID: {book['id']}")
                print(f"Title: {book['title']}")
                print(f"Author(s): {authors}")
                print(f"Downloads: {book['download_count']}")
                # Get preferred format (usually HTML or EPUB)
                formats = book.get('formats', {})
                link = formats.get('text/html') or formats.get('application/epub+zip') or "N/A"
                print(f"Link: {link}")
                print("-" * 30)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
