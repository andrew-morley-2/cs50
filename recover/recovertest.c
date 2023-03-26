#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *forensics = "card.raw";

int main(int argc, char *argv[])
{
    if (strcmp(argv[1], forensics) == 0)
    {
    FILE *file = fopen(argv[1], "r");

    char buffer[512];

    while (fread(buffer, 1, sizeof(buffer), file))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xf0)
        {
            FILE *img = fopen(file, "w");
            sprintf(file, "%03i.jpg", 1);
            fwrite(buffer[4], 1, 512, file);

            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xf0)
            {
                fclose(img);
            }
        }
    }
    }
    else
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
}
