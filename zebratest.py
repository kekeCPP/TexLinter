"""@Author Hampus Grimskär"""
import unittest
import linter
import re

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
        # for word in text:
        #     if word == " ":
        #         text.remove(word)
        # print(text)

        i = 0
        titles = ["mr", "Mr", "ms", "Ms", "miss", "Miss", "dr", "Dr", "pr", "Pr"]
        while i < len(text) - 1:
            if text[i] == "." or text[i] == "?" or text[i] == "!":
                if all(text[i - 1] != title for title in titles):
                    # If the sentence is followed by a capital letter
                    if text[i + 2][0].isupper():
                        self.assertEqual(text[i + 1], "\n")
            i = i + 1

if __name__ == "__main__":
    unittest.main()
