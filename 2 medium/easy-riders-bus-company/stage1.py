import json


class EasyRidersEntry:
    meta = {
        "bus_id": {"type": int, "required": True},
        "stop_id": {"type": int, "required": True},
        "stop_name": {"type": str, "required": True},
        "next_stop": {"type": int, "required": True},
        "stop_type": {"type": "char", "required": False},
        "a_time": {"type": str, "required": True},
    }
    errors = dict.fromkeys(meta, 0)

    def __init__(self, entry: dict):
        self.entry = entry

    def check_fields(self):
        for key, value in self.entry.items():
            meta = self.meta[key]
            if self._is_field_required_ok(value, meta["required"]):
                if value != "" and not self._is_field_type_ok(value, meta["type"]):
                    self.errors[key] += 1
            else:
                self.errors[key] += 1

    @classmethod
    def show_errors(cls):
        print("Type and required field validation:", sum(cls.errors.values()), "errors")
        print(*[f"{k}: {v}" for k, v in cls.errors.items()], sep="\n")

    @staticmethod
    def _is_field_type_ok(value, type_) -> bool:
        return (
            type(value) is type_
            if type_ != "char"
            else type(value) is str and len(value) == 1
        )

    @staticmethod
    def _is_field_required_ok(value, required) -> bool:
        return False if required and value == "" else True


def main():
    [EasyRidersEntry(entry).check_fields() for entry in json.loads(input())]
    EasyRidersEntry.show_errors()


if __name__ == "__main__":
    main()
