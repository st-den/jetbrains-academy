import random

n_friends = int(input("Enter the number of friends joining (including you):\n"))

if n_friends > 0:
    print("\nEnter the name of every friend (including you), each on a new line:")

    friends = dict.fromkeys([input() for _ in range(n_friends)], 0)
    bill = int(input("Enter the total bill value:\n"))

    if (input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n') == "Yes"):
        lucky = random.choice(list(friends))
        print(lucky, "is the lucky one!")

        friends = {f: round(bill / (len(friends) - 1), 2) for f in friends}
        friends[lucky] = 0
    else:
        print("No one is going to be lucky")
        friends = {f: round(bill / len(friends), 2) for f in friends}

    print(friends)
else:
    print("No one is joining for the party")
