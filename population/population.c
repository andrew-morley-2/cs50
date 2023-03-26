#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt for start size

    int s;
    do
    {
        s = get_int("Start size: ");
    }
    while (s < 9);

    // Prompt for end size

    int e;
    do
    {
        e = get_int("End size: ");
    }
    while (e < s);

    // Define starting number of years

    int n = 0;

    // Calculate number of years until we reach threshold

    while (s < e)
    {
        s = s + (s / 3) - (s / 4);
        n += 1;
    }

    // Print number of years

    printf("Years: %i\n", n);
}
