import csv
import sys
import re


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    db = {}
    dbase = []
    # TODO: Read database file into a variable
    with open(sys.argv[1]) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            db.update(row)
            dbase.append(row)

    sequence = []
    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as txtfile:
        txtreader = csv.reader(txtfile)
        for row in txtreader:
            sequence = row

    matches = []
    strand = []
    # TODO: Find longest match of each STR in DNA sequence
    for i in db:
        match = (longest_match(sequence[0], i))
        matches.append(match)
        strand.append(i)

    # TODO: Check database for matching profiles
    with open(sys.argv[1]) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            for i in matches:
                if str(matches[1]) in row[strand[1]] and str(matches[2]) in row['AATG'] and str(matches[3]) in row['TATC']:
                    print(f"{row['name']}")
                    break
                if str(matches[1]) in row[strand[1]] and str(matches[2]) in row[strand[2]] and str(matches[3]) in row[strand[3]] and str(matches[4]) in row[strand[4]] and str(matches[5]) in row[strand[5]] and str(matches[6]) in row[strand[6]] and str(matches[7]) in row[strand[7]]:
                    print(f"{row['name']}")
                    break
                elif row == '\0':
                    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
