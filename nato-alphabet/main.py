# used libraries
import pandas

# read file with NATO phonetic alphabet
data = pandas.read_csv("nato_phonetic_alphabet.csv")

# save data from file to dict
nato_dict = {row.letter: row.code for (index, row) in data.iterrows()}


def generate_phonetic():
    """Generates phonetic letters for a word inputted by user"""

    user_input = input("Enter a word: ")
    try:
        output = [nato_dict[letter] for letter in user_input.upper()]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic()
    else:
        print(output)


generate_phonetic()
