import unittest
from compare import doublebarrel_label_handeling

class testwhatisthis(unittest.TestCase):
    def test_str_ls(self):
        out = doublebarrel_label_handeling("car")
        self.assertTrue(type(out) == list)
    
    def test_str_ls_labels(self):
        with open("imagelabelunit.txt", "r") as labelsf:
            labels = labelsf.readlines()

        for label in labels:
            clean = label.strip("\n")
            with self.subTest(clean=clean):
                out = doublebarrel_label_handeling(clean)
                self.assertTrue(type(out) == list)

    def test_str_none_labels(self):
        with open("imagelabelunit.txt", "r") as labelsf:
            labels = labelsf.readlines()

        for label in labels:
            clean = label.strip("\n")
            with self.subTest(clean=clean):
                out = doublebarrel_label_handeling(clean)
                self.assertTrue(out)


if __name__ == "__main__":
    unittest.main()
