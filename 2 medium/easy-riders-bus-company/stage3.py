import json


def main():
    data = json.loads(input())

    bus_stops = {}
    for d in data:
        bus_stops.setdefault(d["bus_id"], set())
        bus_stops[d["bus_id"]].add(d["stop_id"])

    print("Line names and number of stops:")
    print(
        *[f"bus_id: {k}, stops: {len(v)}" for k, v in bus_stops.items()],
        sep="\n",
    )


if __name__ == "__main__":
    main()
