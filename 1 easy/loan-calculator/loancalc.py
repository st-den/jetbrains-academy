import argparse, sys, math

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str)
parser.add_argument("--payment", type=int)
parser.add_argument("--principal", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
args = parser.parse_args()


def incorrect_params():
    print("Incorrect parameters")
    sys.exit(1)


if len(sys.argv) != 5 or args.interest is None:
    incorrect_params()
else:
    for v in vars(args).values():
        if type(v) in (int, float) and v < 0:
            incorrect_params()

    payment, principal, periods = args.payment, args.principal, args.periods
    nominal_interest = args.interest / (12 * 100)

    if args.type == "annuity":
        if args.payment and args.periods:
            principal = math.floor(
                args.payment
                / (
                    (nominal_interest * pow(1 + nominal_interest, periods))
                    / (pow(1 + nominal_interest, periods) - 1)
                )
            )

            print(f"Your loan principal = {principal}!")
        elif args.payment and args.principal:

            def convert_months_to_human(n_months):
                months = n_months % 12
                years = n_months // 12
                months_word, years_word = None, None

                if months == 1:
                    months_word = "month"
                elif months > 1:
                    months_word = "months"

                if years == 1:
                    years_word = "year"
                elif years > 1:
                    years_word = "years"

                if years and months:
                    return f"{years} {years_word} and {months} {months_word}"
                elif years:
                    return f"{years} {years_word}"
                elif months:
                    return f"{months} {months_word}"

            periods = math.ceil(
                math.log(
                    args.payment / (args.payment - nominal_interest * args.principal),
                    1 + nominal_interest,
                )
            )

            print(
                f"It will take {convert_months_to_human(periods)} to repay this loan!"
            )
        elif args.principal and args.periods:
            payment = math.ceil(
                args.principal
                * (
                    (nominal_interest * pow(1 + nominal_interest, periods))
                    / (pow(1 + nominal_interest, periods) - 1)
                )
            )

            print(f"Your annuity payment = {payment}!")

        print(f"Overpayment = {payment * periods - principal}")
    elif args.type == "diff":
        if args.payment:
            incorrect_params()
        else:
            total = 0

            for month in range(1, periods + 1):
                diff_payment = math.ceil(
                    principal / periods
                    + nominal_interest
                    * (principal - (principal * (month - 1) / periods))
                )

                total += diff_payment

                print(f"Month {month}: payment is {diff_payment}")

            print(f"\nOverpayment = {math.ceil(total) - principal}")
    else:
        incorrect_params()
