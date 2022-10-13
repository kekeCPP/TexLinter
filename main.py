"""@Author Hampus Grimskär"""
import argparse
import os
import re
import json
import sys

def add_newline_after_sentence(text):
    """Function to format text to add a new line after each sentence"""

    # split the text into sections
    split_text = re.split(r"(\\section)", text)
    i = 0
    while i < len(split_text):
        if split_text[i] == "\\section":

            # split the section for every sentence
            words = re.split(r"([ .?!])", split_text[i + 1])
            words = list(filter(None, words))
            titles = ["mr", "Mr", "ms", "Ms", "miss", "Miss", "dr", "Dr", "pr", "Pr"]

            # add a line break after each sentence, join the list to one string
            j = 0
            while j < len(words) - 1:
                if words[j] == "." or words[j] == "?" or words[j] == "!":
                    if all(words[j - 1] != title for title in titles):
                        if words[j + 1] != "\n":
                            if words[j + 1] == " ":
                                # If first letter of the next word is
                                # upper case we can add a newline
                                if words[j + 2][0].isupper():
                                    words[j + 1] = "\n"
                j = j + 1
            words = "".join(words)
            split_text[i + 1] = words

        i = i + 1

    # Change the text variable to match the newly formatted text
    text = ""

    for par in split_text:
        text = text + par

    # Return the formated text
    return text


def add_space_after_comment(text):
    """Function to add a space after each comment in the document"""

    split_text = re.split(r"(%|\\%)", text)
    text = ""

    i = 0
    while i < len(split_text):
        if split_text[i] == "%":
            if split_text[i + 1][0] != " ":
                split_text.insert(i + 1, " ")
        text = text + split_text[i]
        i = i + 1

    # Return the formated text
    return text


def add_lines_before_section(text, amount_of_lines):
    """Function that adds <amount_of_lines> of blank lines before a section or chapter"""
    split_text = re.split(r"(\\section|\n)", text)
    split_text = list(filter(None, split_text))

    i = 0
    while i < len(split_text):
        if split_text[i] == "\\section":

            # Find the amount of blank lines already existing
            j = 1
            count = 0
            while split_text[i - j] == "\n":
                count = count + 1
                j = j + 1

            # Remove blank lines if there are more than wanted
            while count > amount_of_lines + 1:
                del split_text[i - j + 1]
                j = j - 1
                count = count - 1
                i = i - 1

            # Add blank lines if there are less than wanted
            while count < amount_of_lines + 1:
                split_text.insert(i - j + 1, "\n")
                j = j + 1
                count = count + 1
                i = i + 1

        i = i + 1

    # Change the text variable to match the newly formatted text
    text = ""

    for par in split_text:
        text = text + par

    # Return the formated text
    return text

def add_indentations(text):
    """Function that adds indentations for environmental blocks"""

    # Split the text for the useful keywords and remove any instances
    # of tabs or spaces aswell as empty elements
    unfiltered_list = re.split(r"(\\begin|\\end|[{}]|\n)", text)
    split_text = []

    for element in unfiltered_list:
        split_text.append(element.strip(" \t"))

    split_text = list(filter(None, split_text))



    tab_multiplier = 0
    i = 0
    while i < len(split_text):
        # Add indentations and increase the amount of indentations for upcoming elements
        if split_text[i] == "\\begin" and split_text[i + 2] != "document":
            k = 0
            while k < tab_multiplier:
                split_text.insert(i, "\t")
                k = k + 1
                i = i + 1
            tab_multiplier = tab_multiplier + 1

        # Decrease the amount of indentations for upcoming elements and add indentations
        elif split_text[i] == "\\end" and split_text[i + 2] != "document":
            tab_multiplier = tab_multiplier - 1
            k = 0
            while k < tab_multiplier:
                split_text.insert(i, "\t")
                k = k + 1
                i = i + 1

        else:
            # Add indentations if the element is at the beginning of a new line
            if split_text[i] != "\n" and split_text[i - 1] == "\n":
                k = 0
                while k < tab_multiplier:
                    split_text.insert(i, "\t")
                    k = k + 1
                    i = i + 1

        i = i + 1

    # Change the text variable to match the newly formatted text
    text = "".join(split_text)

    # Return the formated text
    return text


def format_text(text):
    """Function that reads the config settings and calls all format functions"""

    # Load data from the config.json file
    with open ("config.json", "r", encoding = "utf-8") as cfg:
        data = json.load(cfg)

    newline_after_sentence = data["newline-after-sentence"]
    space_after_comment = data["space-after-comment"]
    blank_lines_before_section = data["blank-lines-before-section"]
    add_indentations_to_environment_blocks = data["add-indentations-to-environment-blocks"]

    cfg.close()

    # Call the function that adds a new line after every sentence
    if newline_after_sentence:
        text = add_newline_after_sentence(text)

    # Call the function that adds a space after every comment sign
    if space_after_comment:
        text = add_space_after_comment(text)

    # Call the function that adds blank lines before each section and chapter
    text = add_lines_before_section(text, blank_lines_before_section)

    # Call the function that adds indentations to environmental blocks
    if add_indentations_to_environment_blocks:
        text = add_indentations(text)

    # Change type of linebreak based on operating system
    if sys.platform != "win32":
        windows_linebreak = "\r\n"
        unix_linebreak = "\n"
        text = text.replace(windows_linebreak, unix_linebreak)

    # Return the formated text
    return text


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Argument list")

    parser.add_argument("file_path", help = "path to the file you wish to format")
    parser.add_argument("-n", "--newfile", required = False,
    help = "save as a new file at specified path")

    args = parser.parse_args()

    if args.newfile:
        if os.path.exists(args.file_path):
            with open(args.file_path, "r", encoding = "utf-8") as file:
                text = file.read()
                file.close()

            if not os.path.exists(args.newfile):
                with open(args.newfile, "w", encoding = "utf-8") as new_file:
                    text = format_text(text)
                    new_file.write(text)
                    new_file.close()
            else: print("Error: A file with that name already exists!")
    else:
        if os.path.exists(args.file_path):
            with open(args.file_path, "w", encoding = "utf-8") as file:
                file.write("some new text")
                file.close()

if __name__ == "__main__":
    main()
