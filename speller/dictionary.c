// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>

// Global variable definition
int counter;

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Define number of buckets in hash table (number of letters in the alphabet - first two letters in word - 26^2)
const unsigned int N = 676;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Define variable based on the hash of the word to determine correct hash table
    int t = hash(word);

    // Check to make sure the hash table does not have a null value
    if (table[t] != NULL)
    {
        // Create cursor pointer to move through table
        for (node *cursor = table[t]; cursor != NULL; cursor = cursor->next)
        {
            // Compare word with current word that the cursor is pointing to
            if (strcasecmp(word, cursor->word) == 0)
            {
                return true;
            }
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hash word based on the first two letters of the word and the number of buckets (N)
    return ((toupper(word[0]) + toupper(word[1]) - 'A' * 2) % N);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file != NULL)
    {
        // Read strings from file
        char buffer[LENGTH + 1];

        while (fscanf(file, "%s", buffer) != EOF)
        {
            // Create a new node
            node *n = malloc(sizeof(node));
            strcpy(n->word, buffer);

            // Increase counter by 1
            counter++;

            // Hash word
            int i = hash(n->word);

            // Insert node into hash table if the table is null
            if (table[i] == NULL)
            {
                table[i] = n;
            }

            // Insert node into hash table if the table is not null
            else
            {
                n->next = table[i];
                table[i] = n;
            }
        }
        // Close the dictionary
        fclose(file);
        return true;
    }

    else
    {
        return false;
    }
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Check to see if the counter is greater than zero, return value if it is
    if (counter > 0)
    {
        return counter;
    }

    // Return 0 if the above condition is not met
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Go through each hash table
    for (int i = 0; i < (N - 1); i++)
    {
        // Set cursor pointer to the beginning node of the hash table
        node *cursor = table[i];

        // Given the cursor value is not null, create temp pointer to the cursor, move the cursor, and free the temp memory
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
