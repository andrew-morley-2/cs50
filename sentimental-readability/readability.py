from cs50 import get_string


def main():

    # Get text from user
    text = get_string("Text: ")

    # Convert sentences to float
    s = float(count_sentences(text))

    # Convert words to float
    w = float(count_words(text))

    # Convert letters to float
    l = float(count_letters(text))

    # Calculate readability with formula
    index = float(0.0588 * ((l / w) * 100) - 0.296 * ((s / w) * 100) - 15.8)

    # Print the result
    if index >= 1 and index < 16:
        print(f"Grade {index}")

    elif index < 1:
        print("Before Grade 1")

    elif index >= 16:
        print("Grade 16+")


# Count letters function
def count_letters(text):
    l = 0
    for i in range(len(text)):
        if text[i] != ' ' and text[i] != '.' and text[i] != '!' and text[i] != '?':
            l += 1
    return l


# Count words function
def count_words(text):
    w = 1
    for i in range(len(text)):
        if text[i] == ' ':
            w += 1
    return w


# Count sentences function
def count_sentences(text):
    s = 0
    for i in range(len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':
            s += 1
    return s


main()

