import unittest
from compare import whatisthis

class testwhatisthis(unittest.TestCase):
    def test_str_ls(self):
        out = whatisthis("car")
        self.assertTrue(type(out) == list)
    
    def test_str_ls_lables(self):
        with open("imagelableunit.txt", "r") as lablesf:
            lables = lablesf.readlines()

        for lable in lables:
            clean = lable.strip("\n")
            with self.subTest(clean=clean):
                out = whatisthis(clean)
                self.assertTrue(type(out) == list)

    def test_str_none_lables(self):
        with open("imagelableunit.txt", "r") as lablesf:
            lables = lablesf.readlines()

        for lable in lables:
            clean = lable.strip("\n")
            with self.subTest(clean=clean):
                out = whatisthis(clean)
                self.assertTrue(out)



if __name__ == "__main__":
    unittest.main()
