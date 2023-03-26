#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// Declare count letters function
int count_letters(string text);

// Declare count words function
int count_words(string text);

// Declare count sentences function
int count_sentences(string text);

int main(void)
{
// Get text from user
    string text = get_string("Text: ");

// Convert sentences to float
    float s = count_sentences(text);

// Convert words to float
    float w = count_words(text);

// Convert letters to float
    float l = count_letters(text);

// Calculate readability with formula
    float index = 0.0588 * (l / w * 100) - 0.296 * (s / w * 100) - 15.8;

// Print the result
    if (index >= 1 && index < 16)
    {
        printf("Grade %i\n", (int) round(index));
    }

    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }

    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
}

// Count letters function
int count_letters(string text)
{
    float l = 0;

    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isupper(text[i]) || islower(text[i]))
        {
            l++;
        }
    }
    return l;
}

// Count words function
int count_words(string text)
{
    float w = 1;

    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == ' ')
        {
            w++;
        }
    }
    return w;
}

// Count sentences function
int count_sentences(string text)
{
    float s = 0;

    for (int i = 0; text[i] != '\0'; i++)
    {

        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            s++;
        }
    }
    return s;
}