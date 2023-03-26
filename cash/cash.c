#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Ask how many cents the customer is owed
    int cents = get_cents();

    // Calculate the number of quarters to give the customer
    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;

    // Calculate the number of dimes to give the customer
    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

    // Calculate the number of nickels to give the customer
    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;

    // Calculate the number of pennies to give the customer
    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;

    // Sum coins
    int coins = quarters + dimes + nickels + pennies;

    // Print total number of coins to give the customer
    printf("%i\n", coins);
}

// Function to get how many cents the customer is owed
int get_cents(void)
{
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 1);
    return cents;
}

// Function to calculate the amount of quarters owed
int calculate_quarters(int cents)
{
    int quarters = 0;

    while (cents > 24)
    {
        quarters++;
        cents = cents - 25;
    }
    return quarters;
}

// Function to calculate the amount of dimes owed
int calculate_dimes(int cents)
{
    int dimes = 0;

    while (cents > 9)
    {
        dimes++;
        cents = cents - 10;
    }
    return dimes;
}

// Function to calculate the amount of nickels owed
int calculate_nickels(int cents)
{
    int nickels = 0;

    while (cents > 4)
    {
        nickels++;
        cents = cents - 5;
    }
    return nickels;
}

// Function to calculate the amount of pennies owed
int calculate_pennies(int cents)
{
    int pennies = 0;

    while (cents > 0)
    {
        pennies++;
        cents = cents - 1;
    }
    return pennies;
}