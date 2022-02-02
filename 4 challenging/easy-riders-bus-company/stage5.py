import json


def main():
    data = json.loads(input())

    entries_by_bus = dict()
    for d in data:
        entries_by_bus.setdefault(d["bus_id"], [])
        entries_by_bus[d["bus_id"]].append(d)

    print("Arrival time test:")
    ok = True
    for bus, entries in entries_by_bus.items():
        a_time = entries[0]["a_time"]
        for e in entries[1:]:
            if a_time > e["a_time"]:
                print("bus_id line", bus, ": wrong time on station", e["stop_name"])
                ok = False
                break
            a_time = e["a_time"]
    if ok:
        print("OK")


if __name__ == "__main__":
    main()