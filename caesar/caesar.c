#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>

bool only_digits(string s);

char rotate(char c, int n);

int main(int argc, string argv[])
{
// Check to see if argument entry meets standards and provide feedback if it does not
    if (argc != 2 || only_digits(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

// Get string for plaintext from user
    string plaintext = get_string("plaintext: ");

// Print response with actual ciphertext to follow
    printf("ciphertext: ");

// Rotate characters with function for each character in plaintext
    for (int i = 0; plaintext[i] != '\0'; i++)

    {
        if (isupper(plaintext[i]) || (islower(plaintext[i])))
        {
            rotate(plaintext[i], atoi(argv[1]));
        }

        else
        {
            printf("%c", plaintext[i]);
        }
    }

// Print space at end of ciphertext
    printf("\n");

    return 0;
}

// Boolean function to determine if argument conatins only numeric characters
bool only_digits(string s)
{
    for (int i = 0; s[i] != '\0'; i++)
    {
        if (isdigit(s[i]))
        {
            return true;
        }

        else
        {
            return false;
        }
    }
    return 0;
}

// Function to rotate characters based on argument if the character is an uppercase or lowercase letter
char rotate(char c, int n)
{
    if (isupper(c))
    {
        printf("%c", ((c + n - 'A') % 26) + 'A');
    }

    if (islower(c))
    {
        printf("%c", ((c + n - 'a') % 26) + 'a');
    }
    return 0;
}