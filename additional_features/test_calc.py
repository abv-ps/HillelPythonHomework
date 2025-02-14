import unittest
from hw_05.simple_calc import simple_calc


class TestCalcAvg(unittest.TestCase):
    def test_calc_sum(self):
        result = simple_calc(1, '+', 2)
        self.assertEqual(result, 3)

    def test_calc_avg_negative(self):
        result = simple_calc(1, '-', -5)
        self.assertNotEqual(result, -9)
        self.assertEqual(result, 6)

    def test_calc_avg_empty(self):
        result = simple_calc()
        self.assertEqual(result, 0)

    def test_calc_avg_one_element(self):
        result = simple_calc(1)
        self.assertNotEqual(result, 0)
        self.assertEqual(result, 1)

    def test_calc_avg_string(self):
        with self.assertRaises(TypeError):
            simple_calc("string")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
