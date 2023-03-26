#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "wav.h"

char *input = ".wav";

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc == 3 && strstr(argv[1], input))
    {
        // Open input file for reading
        FILE *ifile = fopen(argv[1], "r");

        // Read header
        WAVHEADER header;
        fread(&header, sizeof(WAVHEADER), 1, ifile);

        // Set variable value to end of header
        int endheader = ftell(ifile);

        // Use check_format to ensure WAV format
        check_format(header);

        // Open output file for writing
        FILE *ofile = fopen(argv[2], "w");

        // Write header to file
        fwrite(&header, sizeof(WAVHEADER), 1, ofile);

        // Use get_block_size to calculate size of block
        int size = get_block_size(header);

        // Set variable value to data bytes (minus header)
        int databytes = 352844;

        // Write reversed audio to file
        char buffer[352844];
        fseek(ifile, 0, SEEK_END);
        while (fread(&endheader, size, 1, ifile))
        {
            fwrite(&endheader, size, 1, ofile);
        }

        // Close all files
        fclose(ifile);
        fclose(ofile);
    }

    else
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }
}

int check_format(WAVHEADER header)
{
    // Check to see if file is a WAV file
    if (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E')
    {
        return 0;
    }

    else
    {
        return 1;
    }
}

int get_block_size(WAVHEADER header)
{
    // Get block size
    int size = header.numChannels * header.bitsPerSample / 8;
    return size;
}