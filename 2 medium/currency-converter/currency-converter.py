import requests

url = "http://www.floatrates.com/daily/"

cache = {
    "usd": requests.get(f"{url}usd.json").json(),
    "eur": requests.get(f"{url}eur.json").json(),
}

in_currency = input().lower()

while True:
    out_currency = input().lower()
    if out_currency == "":
        break
    amount = float(input())

    print("Checking the cache...")
    if cache.get(out_currency):
        print("Oh! It is in the cache!")
    else:
        print("Sorry, but it is not in the cache!")
        cache[out_currency] = requests.get(f"{url}{out_currency}.json").json()

    print(
        "You received ",
        round(amount * cache[out_currency][in_currency]["inverseRate"], 2),
        "".join((out_currency.upper(), ".")),
    )
