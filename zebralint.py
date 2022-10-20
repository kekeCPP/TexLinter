"""@Author Hampus Grimskär"""
import argparse
import os
import linter


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Argument list")

    parser.add_argument("file_path", help = "path to the file you wish to format")
    parser.add_argument("-n", "--newfile", required = False,
    help = "save as a new file at specified path")

    args = parser.parse_args()

    file_type = args.file_path[(len(args.file_path) - 4):(len(args.file_path))]

    if args.newfile:
        newfile_type = args.newfile[(len(args.newfile) - 4):(len(args.newfile))]
        if os.path.exists(args.file_path):
            if file_type != ".tex":
                print("Error: The file you are trying to format is of the wrong type!")
            else:
                with open(args.file_path, "r", encoding = "utf-8") as file:
                    text = file.read()
                    file.close()

                if not os.path.exists(args.newfile):
                    if newfile_type != ".tex":
                        print("Error: The new file needs to be of .tex type!")
                    else:
                        with open(args.newfile, "w", encoding = "utf-8") as new_file:
                            text = linter.format_text(text)
                            new_file.write(text)
                            new_file.close()
                else: print("Error: A file with that name already exists!")
        else:
            print("Error: The file you are trying to format doesn't exist!")
    else:
        if os.path.exists(args.file_path):
            if file_type != ".tex":
                print("Error: The file you are trying to format is of the wrong type!")
            else:
                with open(args.file_path, "r", encoding = "utf-8") as file:
                    text = file.read()
                    text = linter.format_text(text)
                    file.close()
                with open(args.file_path, "w", encoding = "utf-8") as file:
                    file.write(text)
                    file.close()
        else:
            print("Error: The file you are trying to format doesn't exist!")

if __name__ == "__main__":
    main()
