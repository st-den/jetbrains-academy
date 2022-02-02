import os
import sys
from collections import defaultdict
from hashlib import md5


def get_size_paths(root_dir: str, file_ext: str, reverse: bool) -> dict[int, list[str]]:
    size_paths: dict[int, list[str]] = defaultdict(list)
    for root, _, files in os.walk(root_dir):
        for name in files:
            path = os.path.join(root, name)
            if file_ext in os.path.splitext(name)[1]:
                size_paths[os.path.getsize(path)].append(path)
    return dict(sorted(size_paths.items(), reverse=reverse))


def show_size_paths(size_paths: dict):
    for size, paths in size_paths.items():
        if len(paths) > 1:
            print(f"\n{size} bytes", *paths, sep="\n")


def get_size_hash_paths(size_paths: dict) -> dict[int, dict[str, list]]:
    size_hash_paths: dict[int, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for size, paths in size_paths.items():
        if len(paths) > 1:
            for file in paths:
                with open(file, "rb") as f:
                    size_hash_paths[size][md5(f.read()).hexdigest()].append(file)
    return size_hash_paths


def show_size_hash_paths(size_hash_paths: dict) -> int:
    idx = 0
    for size, hashes in size_hash_paths.items():
        size_printed = False
        for hash_, paths in hashes.items():
            if len(paths) > 1:
                if not size_printed:
                    print(f"\n{size} bytes")
                    size_printed = True

                print(f"Hash: {hash_}")

                for path in paths:
                    idx += 1
                    print(f"{idx}. {path}")
    return idx


def remove_file_by_idx(size_hash_paths: dict, choice: int) -> int:
    idx = 1
    for size, hashes in size_hash_paths.items():
        for paths in hashes.values():
            if len(paths) > 1:
                for path in paths:
                    if idx == choice:
                        os.remove(path)
                        return size
                    idx += 1
    raise IndexError


def main():
    file_ext = "." + input("Enter file format:\n")

    print("\nSize sorting options:", "1. Descending", "2. Ascending\n", sep="\n")
    while (reverse := input("Enter a sorting option:\n")) == "" or reverse not in "12":
        print("Wrong option\n")

    size_paths = get_size_paths(root_folder, file_ext, reverse == "1")
    show_size_paths(size_paths)

    while (check_duplicates := input("\nCheck for duplicates?\n")) not in ("yes", "no"):
        print("Wrong option\n")

    if check_duplicates == "yes":
        size_hash_paths = get_size_hash_paths(size_paths)
        last_idx = show_size_hash_paths(size_hash_paths)

        if last_idx > 0:
            while (delete_files := input("\nDelete files?\n")) not in ("yes", "no"):
                print("Wrong option\n")

            if delete_files == "yes":
                while True:
                    try:
                        choices = input("\nEnter file numbers to delete:\n").split()

                        if not choices:
                            raise ValueError
                        choices = [int(ch) for ch in choices]
                    except ValueError:
                        print("Wrong option\n")
                    else:
                        if all(1 <= idx <= last_idx for idx in choices):
                            break

                freed = sum(remove_file_by_idx(size_hash_paths, ch) for ch in choices)
                print("Total freed up space:", freed, "bytes")


if __name__ == "__main__":
    try:
        root_folder = sys.argv[1]
    except IndexError:
        print("Directory is not specified")
        sys.exit()
    else:
        main()
