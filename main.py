import json
import os
import random
import string
from urllib.parse import urlparse
import argparse

#we need something that saves data to disk, we will use a json file as its human readable nd part of std lib
DATA_FILE = "data.json"

def load_data():
    #load the url data from the disk. Returns empty dict if file doesnt exist

    if not os.path.exists(DATA_FILE):
        return {}
    
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    #saves the url data to disk

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

'''
we are basically storing a dict in json which would store all the mappings of urls, like this:
{
  "a1b2c3": {
    "url": "https://example1.com",
    "clicks": 0
  },
  "xyz123": {
  "url": "https://example2.com",
  "clicks": 0
  },
  nd so on..
}
'''

def generate_code(data, length=6):
    chars = string.ascii_letters + string.digits
    #so chars="abc...xyzABC...XYZ012...9"

    while True:
        code = ''.join(random.choice(chars) for i in range(length))
        if code not in data:   #making sure the code isnt already used
            return code


def normalise_url(url):
    #if user forgets the scheme, assume https://
    if not urlparse(url).scheme:
        url = "https://" + url
    return url

def is_valid_url(url):
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        if "." not in result.netloc:
            return False
        return True
    except ValueError:
        return False 
'''
if url is "https://example.com/page" then Parseresult(scheme='https', netloc='example.com', path='page',paramas='',query='',fragment='')
all() takes a list and returns True only if every item in it is "truthy" (non-empty, non-zero). 
If any one is empty then returns False
If user types just google.com, then Parseresult(scheme='', netloc='', path='google.com'...)
So we fix it using normalise_url
'''

def shorten(url, alias=None):
    url = normalise_url(url)

    if not is_valid_url(url):
        print(f"Error: The url '{url}' is not valid!")
        return

    data = load_data()

    if alias:
        #alias is nothing but a code given by user. If nothing is provided then code is generated randomly
        if alias in data:
            print(f"Error: alias '{alias}' is already taken!")
            return
        code = alias

    else:
        code = generate_code(data)

    data[code] = {"url": url, "clicks": 0}
    save_data(data)

    print(f"Shortened URL: {url} -> {code}")


def resolve(code):
    data = load_data()

    if code not in data:
        print(f"Error: code {code} not found!")
        return

    data[code]["clicks"] += 1  #for the code given by user, we increased the no of times it has been resolved
    save_data(data)

    print(f"Original URL: {data[code]['url']}")
    print(f"(resolved {data[code]['clicks']} times)")


def list_urls():
    data = load_data()

    if not data:
        print(f"Error: No URLs shortened yet!")
        return

    for code, info in data.items():
        print(f"{code} -> {info['url']}  (clicks: {info['clicks']})")



def main():
    parser = argparse.ArgumentParser(description="Mini URL Shortner")
    subparsers = parser.add_subparsers(dest="command")

    shorten_parser = subparsers.add_parser("shorten", help="Shorten a URL")
    shorten_parser.add_argument("url", help="The long url to shorten")
    shorten_parser.add_argument("--alias", help="custom alias for the short code", default=None)

    resolve_parser = subparsers.add_parser("resolve", help="resolve a short code to its URL")
    resolve_parser.add_argument("code", help="The short code to resolve")

    list_parser = subparsers.add_parser("list", help="List all shortened URLs")


    args = parser.parse_args()

    if args.command == "shorten":
        shorten(args.url, alias=args.alias)
    elif args.command == "resolve":
        resolve(args.code)
    elif args.command == "list":
        list_urls()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

