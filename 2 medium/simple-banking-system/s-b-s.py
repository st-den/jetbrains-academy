import random
import sqlite3


class BankingSystem:
    def __init__(self, db_file_name):
        self._db_connector, self._db_cursor = None, None
        self._init_db(db_file_name)

        self._logged_in, self._id, self._number, self._pin, self._balance = (
            False,
            None,
            None,
            None,
            0,
        )

        self._message_logged_out = (
            "1. Create an account\n2. Log into account\n0. Exit\n"
        )
        self._functions_logged_out = {
            1: self._create_account,
            2: self._log_in,
            0: self._exit,
        }
        self._message_logged_in = "1. Balance\n2. Add income\n3. Make transfer\n4. Close account\n5. Log out\n0. Exit\n"
        self._functions_logged_in = {
            1: self._get_balance,
            2: self._add_balance,
            3: self._make_transfer,
            4: self._close_account,
            5: self._log_out,
            0: self._exit,
        }

        while True:
            self._menu()

    def _init_db(self, file_name):
        empty = False
        try:
            with open(file_name, "x"):
                pass
            empty = True
        except FileExistsError:
            pass

        self._db_connector = sqlite3.connect(file_name)
        self._db_cursor = self._db_connector.cursor()

        if empty:
            self._db_cursor.execute(
                """
                CREATE TABLE card (
                    id INTEGER PRIMARY KEY,
                    number TEXT,
                    pin TEXT,
                    balance INTEGER DEFAULT 0)
                """
            )
            self._db_connector.commit()

    def _menu(self):
        if self._logged_in:
            choice = int(input(self._message_logged_in))
            functions = self._functions_logged_in
        else:
            choice = int(input(self._message_logged_out))
            functions = self._functions_logged_out

        print()
        try:
            functions[choice]()
        except KeyError:
            print("Invalid input")
        print()

    def _create_account(self):
        # NOTTODO: check db for duplicates :)

        card_number = self._generate_card_number()
        card_number += self._generate_luhn_checksum(card_number)
        pin = self._generate_card_pin()

        self._db_cursor.execute(
            f"INSERT INTO card (number, pin) VALUES {(card_number, pin)}"
        )
        self._db_connector.commit()

        print(
            "Your card has been created",
            "Your card number:",
            card_number,
            "Your card PIN:",
            pin,
            sep="\n",
        )

    def _log_in(self):
        card_number = input("Enter your card number:\n")
        pin = input("Enter your PIN:\n")

        self._db_cursor.execute(
            f"SELECT id, number, pin, balance FROM card WHERE number = {card_number} AND pin = {pin}"
        )

        try:
            (
                self._id,
                self._number,
                self._pin,
                self._balance,
            ) = self._db_cursor.fetchone()
        except TypeError:
            print("\nWrong card number or PIN!")
        else:
            self._logged_in = True
            print("\nYou have successfully logged in!")

    def _exit(self):
        print("Bye!")
        self._db_connector.close()
        exit()

    def _get_balance(self):
        print(f"Balance: {self._balance}")

    def _add_balance(self):
        income = int(input("Enter income:\n"))
        self._balance += income
        print("Income was added!")

        self._db_cursor.execute(
            f"UPDATE card SET balance = {self._balance} WHERE id = {self._id}"
        )
        self._db_connector.commit()

    def _make_transfer(self):
        receiver_number = input("Transfer\nEnter card number:\n")

        if receiver_number[-1] != self._generate_luhn_checksum(receiver_number[:-1]):
            print("Probably you made a mistake in the card number. Please try again!")
        else:
            self._db_cursor.execute(
                f"SELECT number FROM card WHERE number = {receiver_number}"
            )
            if self._db_cursor.fetchone():
                transfer_amount = int(
                    input("Enter how much money you want to transfer:\n")
                )

                if transfer_amount > self._balance:
                    print("Not enough money!")
                else:
                    self._db_cursor.execute(
                        f"UPDATE card SET balance = {transfer_amount} WHERE number = {receiver_number}"
                    )
                    self._db_connector.commit()

                    self._balance -= transfer_amount
                    self._db_cursor.execute(
                        f"UPDATE card SET balance = {self._balance} WHERE id = {self._id}"
                    )
                    self._db_connector.commit()

                    print("Success!")
            else:
                print("Such a card does not exist.")

    def _close_account(self):
        self._db_cursor.execute(f"DELETE FROM card WHERE id = {self._id}")
        self._db_connector.commit()

        print("The account has been closed!")
        self._logged_in = False

    def _log_out(self):
        self._logged_in = False
        print("You have successfully logged out!")

    @staticmethod
    def _generate_card_number():
        return f"400000{random.randint(0,999999999):09d}"

    @staticmethod
    def _generate_card_pin():
        return f"{random.randint(0,9999):04d}"

    @staticmethod
    def _generate_luhn_checksum(card_number):
        total = sum(int(d) for d in card_number[1::2])
        for d in card_number[::2]:
            prod = int(d) * 2
            total += prod - 9 if prod > 9 else prod

        return str((10 - total % 10) % 10)


def main():
    BankingSystem("card.s3db")


if __name__ == "__main__":
    main()
