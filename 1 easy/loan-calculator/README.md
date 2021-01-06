# Loan Calculator

Project page: https://hyperskill.org/projects/90

## Usage

1. **Calculate differentiated payment**

    ```powershell
    > loancalc.py --type=diff --principal=10000 --periods=12 --interest=5.5
    ```

    ```
    Month 1: payment is 880
    Month 2: payment is 876
    Month 3: payment is 872
    Month 4: payment is 868
    Month 5: payment is 864
    Month 6: payment is 861
    Month 7: payment is 857
    Month 8: payment is 853
    Month 9: payment is 849
    Month 10: payment is 845
    Month 11: payment is 841
    Month 12: payment is 838

    Overpayment = 304
    ```

2. **Calculate annuity payment** (given principal and number of payments)

    ```powershell
    > loancalc.py --type=annuity --principal=100000 --periods=60 --interest=3  
    ```

    ```
    Your annuity payment = 1797!
    Overpayment = 7820
    ```

3. **Calculate loan principal** (given annuity payment and number of payments)

    ```powershell
    > loancalc.py --type=annuity --payment=1000 --periods=12 --interest=10
    ```

    ```
    Your loan principal = 11374!
    Overpayment = 626
    ```

4. **Calculate number of payments** (given annuity payment and principal)

    ```powershell
    > loancalc.py --type=annuity --principal=500000 --payment=5000 --interest=7  
    ```

    ```
    It will take 12 years and 7 months to repay this loan!
    Overpayment = 255000
    ```
