#include <cs50.h>
#include <stdio.h>

int get_height(void);
void print_blocks(int size);

int main(void)
{
    // Get height

    int h = get_height();

    // Print blocks

    print_blocks(h);
}

// Individual function for height prompt
int get_height(void)
{
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);
    return h;
}

// Individual function for block print
void print_blocks(int size)
{

// Initial if statement for a single block

    if (size == 1)
    {
        printf("#");
        printf("\n");
    }

// Else if statement for additional layer (based on height input of 2)

    else if (size == 2)
    {
        printf(" #\n##");
        printf("\n");
    }

// Else if statement for additional layer (based on height input of 3)

    else if (size == 3)
    {
        printf("  #\n ##\n###");
        printf("\n");
    }

// Else if statement for additional layer (based on height input of 4)

    else if (size == 4)
    {
        printf("   #\n  ##\n ###\n####");
        printf("\n");
    }

// Else if statement for additional layer (based on height input of 5)

    else if (size == 5)
    {
        printf("    #\n   ##\n  ###\n ####\n#####");
        printf("\n");
    }

// Else if statement for additional layer (based on height input of 6)

    else if (size == 6)
    {
        printf("     #\n    ##\n   ###\n  ####\n #####\n######");
        printf("\n");
    }

// Else if statement for additional layer (based on height input of 7)

    else if (size == 7)
    {
        printf("      #\n     ##\n    ###\n   ####\n  #####\n ######\n#######");
        printf("\n");
    }

// Else if statement for additional layer (based on height input of 8)

    else if (size == 8)
    {
        printf("       #\n      ##\n     ###\n    ####\n   #####\n  ######\n #######\n########");
        printf("\n");
    }
}