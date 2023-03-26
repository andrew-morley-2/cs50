#include "helpers.h"
#include <math.h>

int swap(int x, int y);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

// Set float variable for each pixel's color value
            float r = image[i][j].rgbtRed;
            float g = image[i][j].rgbtGreen;
            float b = image[i][j].rgbtBlue;

// Add pixel color sum, divide by 3, and round value
            {
                image[i][j].rgbtRed = round((r + g + b) / 3.0);
                image[i][j].rgbtGreen = round((r + g + b) / 3.0);
                image[i][j].rgbtBlue = round((r + g + b) / 3.0);
            }
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float r = image[i][j].rgbtRed;
            float g = image[i][j].rgbtGreen;
            float b = image[i][j].rgbtBlue;

            int sr = round(.393 * r + .769 * g + .189 * b);

// Set red value per pixel with max value of 255
            if (isless(sr, 255.0))
            {
                image[i][j].rgbtRed = sr;
            }

            if (isgreater(sr, 255.0))
            {
                image[i][j].rgbtRed = 255;
            }

// Set green value per pixel with max value of 255
            int sg = round(.349 * r + .686 * g + .168 * b);

            if (isless(sg, 255.0))
            {
                image[i][j].rgbtGreen = sg;
            }

            if (isgreater(sg, 255.0))
            {
                image[i][j].rgbtGreen = 255;
            }

// Set blue value per pixel with max value of 255
            int sb = round(.272 * r + .534 * g + .131 * b);

            if (isless(sb, 255.0))
            {
                image[i][j].rgbtBlue = sb;
            }

            if (isgreater(sb, 255.0))
            {
                image[i][j].rgbtBlue = 255;
            }
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i <= height; i++)
    {
        for (int j = 0; j < width; j++)
        {

// Swap pixels using temporary variable
            RGBTRIPLE k = image[i][j];
            image[i][j] = image[i][width - j - 1];

// Use temporary variable for each half of image
            if (j < width / 2)
            {
                image[i][j] = k;
            }

            if (j > width / 2)
            {
                image[i][width - j - 1] = k;
            }
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 1; i <= height; i++)
    {
        for (int j = 0; j <= width; j++)
        {

// Calculate sum of pixel and 8 surrounding pixels
            float r = image[i][j].rgbtRed + image[i + 1][j].rgbtRed + image[i + 1][j + 1].rgbtRed
                      + image[i + 1][j - 1].rgbtRed + image[i][j + 1].rgbtRed + image[i - 1][j].rgbtRed
                      + image[i - 1][j - 1].rgbtRed + image[i - 1][j + 1].rgbtRed + image[i][j - 1].rgbtRed;

            float g = image[i][j].rgbtGreen + image[i + 1][j].rgbtGreen + image[i + 1][j + 1].rgbtGreen
                      + image[i + 1][j - 1].rgbtGreen + image[i][j + 1].rgbtGreen + image[i - 1][j].rgbtGreen
                      + image[i - 1][j - 1].rgbtGreen + image[i - 1][j + 1].rgbtGreen + image[i][j - 1].rgbtGreen;

            float b = image[i][j].rgbtBlue + image[i + 1][j].rgbtBlue + image[i + 1][j + 1].rgbtBlue
                      + image[i + 1][j - 1].rgbtBlue + image[i][j + 1].rgbtBlue + image[i - 1][j].rgbtBlue
                      + image[i - 1][j - 1].rgbtBlue + image[i - 1][j + 1].rgbtBlue + image[i][j - 1].rgbtBlue;

// Take sum of surrounding pixel colors, divide, and round
            if (i != 0 || j != 0 || i != height || j != width || i != 1 || j != 1 || i != height - 1 || j != width - 1)
            {
                image[i][j].rgbtRed = round(r / 9.0);
                image[i][j].rgbtGreen = round(g / 9.0);
                image[i][j].rgbtBlue = round(b / 9.0);
            }
        }
    }
}
