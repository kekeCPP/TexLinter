"""@Author Hampus Grimskär"""
import argparse
import os
import re
import json


def add_newline_after_sentence(text):
    """Function to format text to add a new line after each sentence"""

    # split the text into sections
    split_text = re.split(r"(\\section)", text)
    i = 0
    while i < len(split_text):
        if split_text[i] == "\\section":
            # split the section for every sentence
            sentences = re.split(r"((?<=[.!?])|(?<=[.!?]\")) +(?=[A-Z])", split_text[i + 1])
            sentences = list(filter(None, sentences))
            new_sentences = []
            j = 0
            # add a line break after each sentence, join the list to one string
            # and then add it to the split_text list
            while j < len(sentences):
                new_sentences.append(sentences[j])
                # if we are not on the last sentence in the section
                if j < len(sentences) - 1:
                    last_letter = new_sentences[j][len(new_sentences[j]) - 1]
                    if last_letter != r"\n":
                        new_sentences.append(r"\r\n")
                j = j + 1
            new_sentences = "".join(new_sentences)
            split_text[i + 1] = new_sentences
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


def add_lines_before_section(text, amount):
    """Function that adds <amount> of blank lines before a section or chapter"""
    # split_text = re.split(r"(\\\\\n|\\\\|\\|[{}])", text)
    # split_text = re.split(r"([\\{}])", text)
    # split_text = list(filter(None, split_text))
    # text = ""
    # i = 0
    # print(split_text)
    # while i < len(split_text):
    #     if (split_text[i] == "section" and split_text[i - 1] == "\\"):
    #         j = 2
    #         while (j / 2) <= amount:
    #             if split_text[i - j] != "\n" and split_text[i - j] != r"\vspace{\baselineskip}":
    #             # if split_text[i - j] != "\vspace{\baselineskip}":
    #                 split_text.insert((i - j) + 1 + (j - 2), "\n")
    #                 split_text.insert((i - j) + 1 + (j - 2), r"\vspace{\baselineskip}")
    #             j = j + 2
    #     i = i + 1

    split_text = re.split(r"(\\section|\n)", text)
    split_text = list(filter(None, split_text))
    i = 0
    text = ""
    while i < len(split_text):
        if split_text[i] == r"(\\section)":
            j = 1
            count = 0
            while count <= amount:
                if split_text[i - j] != "\n":
                    split_text.insert(i - j)
                count = count + 1
                # split_text.insert((i - j) + 1 + (j - 1), "\n")
                # split_text.insert((i - j) + 1 + (j - 1), r"\vspace{\baselineskip}")
                j = j + 1
        i = i + 1
    print(split_text)

    for par in split_text:
        text = text + par

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

    text = add_lines_before_section(text, 5)

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
