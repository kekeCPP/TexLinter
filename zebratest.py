"""@Author Hampus Grimskär"""
import unittest
import re
import linter

class TestLinterRules(unittest.TestCase):
    """Test Class"""
    def test_file_reading(self):
        """Test if the file could be read"""
        with open("test.tex", encoding = "utf-8") as testfile:
            text = testfile.read()
            testfile.close()
        self.assertNotEqual(text, "")

    def test_newline_after_sentence(self):
        """Test the add_newline_after_sentence function"""
        with open("test.tex", encoding = "utf-8") as testfile:
            text = testfile.read()
            testfile.close()

        text = linter.add_newline_after_sentence(text)
        text = re.split(r"([ .?!\n])", text)
        text = list(filter(None, text))
        i = 0
        titles = ["mr", "Mr", "ms", "Ms", "miss", "Miss", "dr", "Dr", "pr", "Pr"]

        while i < len(text) - 1:
            if text[i] == "." or text[i] == "?" or text[i] == "!":
                if all(text[i - 1] != title for title in titles):
                    # Make sure there is a newline where a sentence ends
                    if text[i + 2][0].isupper():
                        self.assertEqual(text[i + 1], "\n")

                # Make sure there is no new line after the titles
                if any(text[i - 1] == title for title in titles):
                    self.assertNotEqual(text[i + 1], "\n")

                # Look for any potential case where there has been added a newline
                # to a decimal number
                # Note: Test will fail if a sentence ends with a number and the next
                # one begins with a number.
                if text[i - 1].isdigit() and text[i + 2].isdigit():
                    self.assertNotEqual(text[i + 1], "\n")

            # Make sure there is no newline after an abbreviation
            if text[i][0].islower() and text[i - 2] == ".":
                self.assertNotEqual(text[i - 1], "\n")
            i = i + 1

    def test_space_after_comment(self):
        """Test the add_space_after_comment function"""
        with open("test.tex", encoding = "utf-8") as testfile:
            text = testfile.read()
            testfile.close()
        text = linter.add_space_after_comment(text)

        text = re.split(r"(%|\\%)", text)
        i = 0
        while i < len(text) - 1:
            # Make sure there is a space after the comment
            if text[i] == "%":
                self.assertEqual(text[i + 1][0], " ")
            i = i + 1

    def test_lines_before_section(self):
        """Test the add_lines_before_section function"""
        with open("test.tex", encoding = "utf-8") as testfile:
            text = testfile.read()
            testfile.close()
        number_of_lines = 10
        text = linter.add_lines_before_section(text, number_of_lines)

        text = re.split(r"(\\section|\n)", text)
        text = list(filter(None, text))

        # Make sure there are a correct number of new lines before the section
        i = 0
        while i < len(text) - 1:
            if text[i] == "\\section":
                j = 1
                while j <= number_of_lines + 1:
                    self.assertEqual(text[i - j], "\n")
                    j = j + 1
            i = i + 1

    def test_indentations(self):
        """Test the add_indentations function"""
        with open("test.tex", encoding = "utf-8") as testfile:
            text = testfile.read()
            testfile.close()
        text = linter.add_indentations(text)

        text = re.split(r"(\\begin|\\end|[{}]|\n|\t)", text)
        text = list(filter(None, text))
        print(text)
        # Make sure there are a correct number of indentations
        i = 0
        while i < len(text) - 1:
            if text[i] == "center1":
                self.assertEqual(text[i - 1], "\t")
            if text[i] == "center2":
                self.assertEqual(text[i - 1], "\t")
                self.assertEqual(text[i - 2], "\t")
            if text[i] == "center3":
                self.assertEqual(text[i - 1], "\t")
                self.assertEqual(text[i - 2], "\t")
                self.assertEqual(text[i - 3], "\t")
            i = i + 1

if __name__ == "__main__":
    unittest.main()
