import argparse
import os

parser = argparse.ArgumentParser(description="Argument list")

parser.add_argument("file_path")
parser.add_argument("-n", "--newfile", required = False, help = "save as a new file at specified path")

args = parser.parse_args()

def main():
    if (args.newfile):
        if (os.path.exists(args.file_path)):
            with open(args.file_path, "r") as file:
                text = file.read()
                file.close()

            if (not os.path.exists(args.newfile)):
                with open(args.newfile, "w") as new_file:
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