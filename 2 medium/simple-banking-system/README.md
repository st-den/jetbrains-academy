# Simple Banking System

Project page: https://hyperskill.org/projects/109

## Usage example

1. **First guy**

    ```shell
    1. Create an account
    2. Log into account
    0. Exit
    > 1

    Your card has been created
    Your card number:
    4000009052164731
    Your card PIN:
    6171

    1. Create an account
    2. Log into account
    0. Exit
    > 2

    Enter your card number:
    > 4000009052164731
    Enter your PIN:
    > 6171

    You have successfully logged in!

    1. Balance
    2. Add income
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 2

    Enter income:
    > 1234
    Income was added!

    1. Balance
    2. Add income
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 0

    Bye!
    ```

2. **Second guy**

    ```shell
    1. Create an account
    2. Log into account
    0. Exit
    > 1

    Your card has been created
    Your card number:
    4000003997357294
    Your card PIN:
    7878


    1. Create an account
    2. Log into account
    0. Exit
    > 2

    Enter your card number:
    > 4000003997357294
    Enter your PIN:
    > 7878

    You have successfully logged in!

    1. Balance
    2. Add income
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 1

    Balance: 0

    1. Balance
    2. Add income
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 5

    You have successfully logged out!
    ```

3. **First guy**

    ```shell
    1. Create an account
    2. Log into account
    0. Exit
    > 2

    Enter your card number:
    > 4000009052164731
    Enter your PIN:
    > 6171

    You have successfully logged in!

    1. Balance
    2. Add income 
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 3

    Transfer
    Enter card number:
    > 4000003997357290 
    Probably you made a mistake in the card number. Please try again!

    1. Balance
    2. Add income
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 3

    Transfer
    Enter card number:
    > 4000003997357294
    Enter how much money you want to transfer:
    > 10000
    Not enough money!

    1. Balance
    2. Add income
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 3

    Transfer
    Enter card number:
    > 4000003997357294
    Enter how much money you want to transfer:
    > 100
    Success!

    1. Balance
    2. Add income
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 1

    Balance: 1134

    1. Balance
    2. Add income
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 4

    The account has been closed!
    ```

4. **Second guy**

    ```shell
    1. Create an account
    2. Log into account
    0. Exit
    > 2

    Enter your card number:
    > 4000003997357294
    Enter your PIN:
    > 7878

    You have successfully logged in!

    1. Balance
    2. Add income
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 1

    Balance: 100

    1. Balance
    2. Add income
    3. Make transfer
    4. Close account
    5. Log out
    0. Exit
    > 3

    Transfer
    Enter card number:
    > 4000009052164731
    Such a card does not exist.
    ```
