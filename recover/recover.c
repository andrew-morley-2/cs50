#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *forensics = "card.raw";

int main(int argc, char *argv[])
{
    if (strcmp(argv[1], forensics) == 0)
    {
    FILE *file = fopen(argv[1], "r");
    if (file != NULL)
    {
        char c;
        while (fread(&c, 512, 1, file))
        {
            printf("%c", c);
        }
        fclose(file);
    }
    }
    else
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
}