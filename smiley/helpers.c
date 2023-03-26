#include "helpers.h"
#include <stdio.h>
#include <stdlib.h>

// Function to add color to the image
void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // Change all black pixels to a color of your choosing (Red)
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            if (image[i][j].rgbtRed == 0)
            {
                image[i][j].rgbtRed = 255;
            }
        }
    }
}
