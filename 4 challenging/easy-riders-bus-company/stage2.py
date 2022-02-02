import json
import re


class EasyRidersEntry:
    meta = {
        "bus_id": {"type": int, "required": True},
        "stop_id": {"type": int, "required": True},
        "stop_name": {
            "type": str,
            "required": True,
            "format": re.compile(r"^([A-Z][a-z]+ )+(Road|Avenue|Boulevard|Street)$"),
        },
        "next_stop": {"type": int, "required": True},
        "stop_type": {
            "type": "char",
            "required": False,
            "format": re.compile(r"^[SOF]?$"),
        },
        "a_time": {
            "type": str,
            "required": True,
            "format": re.compile(r"^([01]\d|2[0-3]):[0-5]\d$"),
        },
    }
    errors = dict.fromkeys(meta, 0)

    def __init__(self, entry: dict):
        self.entry = entry

    def check_fields(self):
        for key, value in self.entry.items():
            format_ = self.meta[key].get("format")
            if format_ and not self._is_field_format_ok(value, format_):
                self.errors[key] += 1

    @classmethod
    def show_errors(cls):
        print("Format validation:", sum(cls.errors.values()), "errors")
        for k, v in cls.errors.items():
            if cls.meta[k].get("format"):
                print(f"{k}: {v}")

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

    @staticmethod
    def _is_field_format_ok(value, format_: re.Pattern) -> bool:
        return format_.match(value) is not None


def main():
    [EasyRidersEntry(entry).check_fields() for entry in json.loads(input())]
    EasyRidersEntry.show_errors()


if __name__ == "__main__":
    main()
