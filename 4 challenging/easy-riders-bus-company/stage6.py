import json
import itertools


def main():
    data = json.loads(input())

    stops_by_type = {}
    for d in data:
        stops_by_type.setdefault(d["stop_type"], [])
        stops_by_type[d["stop_type"]].append(d["stop_name"])

    transfer_stops = []
    for name in set(itertools.chain(*stops_by_type.values())):
        if list(itertools.chain(*stops_by_type.values())).count(name) > 1:
            transfer_stops.append(name)

    print("On demand stops test:")
    results = set(stops_by_type.get("O", [])) & set(
        itertools.chain(
            stops_by_type.get("S", []),
            stops_by_type.get("F", []),
            stops_by_type.get("", []),
            transfer_stops,
        )
    )
    print("Wrong stop type:", sorted(results)) if results else print("OK")


if __name__ == "__main__":
    main()
