from cs50 import get_int


def main():

    # Get height

    size = get_height()

    # Print blocks

    print_blocks(size)


def get_height():
    while True:
        height = get_int("Height: ")
        if height > 0 and height < 9:
            return height


def print_blocks(size):

    # Initial if statement for a single block
    if size == 1:
        print("#")

    # Else if statement for additional layer (based on height input of 2)
    elif size == 2:
        print(" #\n##")

    # Else if statement for additional layer (based on height input of 3)
    elif size == 3:
        print("  #\n ##\n###")

    # Else if statement for additional layer (based on height input of 4)
    elif size == 4:
        print("   #\n  ##\n ###\n####")

    # Else if statement for additional layer (based on height input of 5)
    elif size == 5:
        print("    #\n   ##\n  ###\n ####\n#####")

    # Else if statement for additional layer (based on height input of 6)
    elif size == 6:
        print("     #\n    ##\n   ###\n  ####\n #####\n######")

    # Else if statement for additional layer (based on height input of 7)
    elif size == 7:
        print("      #\n     ##\n    ###\n   ####\n  #####\n ######\n#######")

    # Else if statement for additional layer (based on height input of 8)
    elif size == 8:
        print("       #\n      ##\n     ###\n    ####\n   #####\n  ######\n #######\n########")


main()