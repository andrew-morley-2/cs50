#include <cs50.h>
#include <stdio.h>

int main(void)
{

    //Prompt user for name
    string s = get_string("What's your name? ");

    //Say hello to user and use their name
    printf("hello, %s\n", s);
}