from cs50 import get_float


def main():
    # Ask how many cents the customer is owed
    cents = get_cents()

    # Calculate the number of quarters to give the customer
    quarters = calculate_quarters(cents)
    cents = round(cents, 2) - quarters * .25

    # Calculate the number of dimes to give the customer
    dimes = calculate_dimes(cents)
    cents = round(cents, 2) - dimes * .10

    # Calculate the number of nickels to give the customer
    nickels = calculate_nickels(cents)
    cents = round(cents, 2) - nickels * .05

    # Calculate the number of pennies to give the customer
    pennies = calculate_pennies(cents)

    # Sum coins
    coins = quarters + dimes + nickels + pennies

    # Print total number of coins to give the customer
    print(f"{coins}")


# Function to get how many cents the customer is owed
def get_cents():
    while True:
        cents = get_float("Change owed: ")
        if cents > 0:
            return cents


# Function to calculate the amount of quarters owed
def calculate_quarters(cents):
    quarters = 0
    while cents > 0.24:
        quarters += 1
        cents = cents - 0.25
    return quarters


# Function to calculate the amount of dimes owed
def calculate_dimes(cents):
    dimes = 0
    while cents > 0.09:
        dimes += 1
        cents = cents - 0.10
    return dimes


# Function to calculate the amount of nickels owed
def calculate_nickels(cents):
    nickels = 0
    while cents > 0.04:
        nickels += 1
        cents = cents - 0.05
    return nickels


# Function to calculate the amount of pennies owed
def calculate_pennies(cents):
    pennies = 0
    while cents > 0:
        pennies += 1
        cents = cents - 0.01
    return pennies


main()