import json


def main():
    data = json.loads(input())

    entries_by_bus = dict()
    for d in data:
        entries_by_bus.setdefault(d["bus_id"], [])
        entries_by_bus[d["bus_id"]].append(d)

    for bus, entries in entries_by_bus.items():
        start_stops, end_stops = 0, 0
        for e in entries:
            if e["stop_type"] == "S":
                start_stops += 1
            elif e["stop_type"] == "F":
                end_stops += 1
        if start_stops != 1 or end_stops != 1:
            return print(f"There is no start or end stop for the line: {bus}.")

    all_stops, start_stops, transfer_stops, finish_stops = [], [], [], []
    for d in data:
        all_stops.append(d["stop_name"])
        if d["stop_type"] == "S":
            start_stops.append(d["stop_name"])
        elif d["stop_type"] == "F":
            finish_stops.append(d["stop_name"])

    for name in set(all_stops):
        if all_stops.count(name) > 1:
            transfer_stops.append(name)

    transfer_stops.sort()
    start_stops = sorted(set(start_stops))
    finish_stops = sorted(set(finish_stops))

    print("Start stops:", len(start_stops), start_stops)
    print("Transfer stops:", len(transfer_stops), transfer_stops)
    print("Finish stops:", len(finish_stops), finish_stops)


if __name__ == "__main__":
    main()