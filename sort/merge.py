def main():
    x = '54187263'

    print(merge(x))

def merge(var):
    length = len(var)

    if length == 1:
        quit()

    else:
        for i in var(0, (length/2)):
            if var[i] > var[i + 1]:
                var[i], var[i + 1] = var[i + 1], var[i]

        for i in var((length/2), length):
            if var[i] > var[i + 1]:
                var[i], var[i + 1] = var[i + 1], var[i]


main()