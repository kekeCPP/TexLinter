"""@Author Hampus Grimskär"""
import argparse
import os
import re
import json

parser = argparse.ArgumentParser(description="Argument list")

parser.add_argument("file_path", help = "path to the file you wish to format")
parser.add_argument("-n", "--newfile", required = False,
help = "save as a new file at specified path")

args = parser.parse_args()


def add_newline_after_sentence(text):
    """Function to format text to add a new line after each sentence"""

    # Split the text to seperate tags and text
    split_text = re.split(r"([\\{}])", text)

    # Check if we are inside of a \section tag
    i = 0
    while i < len(split_text):
        if (split_text[i] == "section" and split_text[i - 1] == "\\"):
            # Split the text for every sentence
            paragraph = re.split(r"((?<=[.!?])|(?<=[.!?]\")) +(?=[A-Z])", split_text[i + 4])

            # Add a new line after every sentence
            j = 0
            paragraph_string = ""
            while j < len(paragraph):
                if paragraph[j] != "":
                    last_letter = paragraph[j][len(paragraph[j]) - 1]
                if (last_letter == "." or last_letter == "?" or last_letter == "!"):
                    paragraph.insert(j + 1, r"\\ ")
                paragraph_string = paragraph_string + paragraph[j]
                j = j + 1
            split_text[i + 4] = paragraph_string
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

    return text


def format_text(text):
    """Function that reads the config settings and calls all format functions"""

    # Load data from the config.json file
    with open ("config.json", "r", encoding = "utf-8") as cfg:
        data = json.load(cfg)

    newline_after_sentence = data["newline-after-sentence"]
    space_after_comment = data["space-after-comment"]

    cfg.close()

    # Call the function that adds a new line after every sentence
    if newline_after_sentence:
        text = add_newline_after_sentence(text)

    # Call the function that adds a space after every comment sign
    if space_after_comment:
        text = add_space_after_comment(text)

    # Return the formated text
    return text


def main():
    """Main function"""

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
