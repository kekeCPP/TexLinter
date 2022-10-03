import argparse
import os
import re
import json

parser = argparse.ArgumentParser(description="Argument list")

parser.add_argument("file_path", help = "path to the file you wish to format")
parser.add_argument("-n", "--newfile", required = False, help = "save as a new file at specified path")

args = parser.parse_args()



def add_newline_after_sentence(text):
# Format text to add a new line after each sentence
    sentences = []
    split_text = re.split(r"([.?!])", text)

    for s in split_text:
        sentences.append(s.strip())
        if (s == "." or s == "?" or s == "!"):
            sentences.append("\n")
    
    text = ""

    for s in sentences:
        text = text + s

    # Return the formated text
    return text
    

def format(text):
    # Load data from the config.json file
    with open ("config.json") as cfg:
        data = json.load(cfg)
    
    newline_after_sentence = data["newline-after-sentence"]

    cfg.close()

    # Call the function that adds a new line after every sentence
    if (newline_after_sentence):
        text = add_newline_after_sentence(text)

    # Return the formated text
    return text


def main():

    if (args.newfile):
        if (os.path.exists(args.file_path)):
            with open(args.file_path, "r") as file:
                text = file.read()
                file.close()

            if (not os.path.exists(args.newfile)):
                with open(args.newfile, "w") as new_file:
                    text = format(text)
                    new_file.write(text)
                    new_file.close()
            else: print("Error: A file with that name already exists!")
    else:
        if (os.path.exists(args.file_path)):
            with open(args.file_path, "w") as file:
                file.write("some new text")
                file.close()

if __name__ == "__main__":
    main()