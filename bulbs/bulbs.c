#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int decimal);

void convert_binary(string message);

int main(void)
{
// Get message from user
    string message = get_string("Message: ");

    (convert_binary(message));

}

void print_bulb(int decimal)
{
    if (decimal == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (decimal == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}

void convert_binary(string message)
{
    for (int i = 0; message[i] != '\0'; i++)
    {
        for (int j = 8; j > 0; j--)
        {
        int pwr = pow(2, j);

        if ((message[i] - pwr) % 2 == 0)
        {
            printf("0");
            message[i] = message[i] / 2;
        }

        else
        {
            message[i] = (message[i] - 1) / 2;
            printf("1");
        }

        if (j == 1)
        {
            printf("\n");
        }
        }
    }
}
