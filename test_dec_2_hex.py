import unittest
import dec_2_hex as dh
class averageTestCase(unittest.TestCase):

    def test_average1(self):
        answer = dh.decimal_to_hexadecimal(100)
        self.assertEqual(answer, "0x64")

    def test_average2(self):
        answer = dh.decimal_to_hexadecimal(1)
        self.assertEqual(answer, "0x1")
    if __name__ == "__main__":
        unittest.main()
