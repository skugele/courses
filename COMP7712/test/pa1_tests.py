from unittest import TestCase

from pa1 import Polynomial


class PolynomialTest(TestCase):

    def test_init(self):
        p1 = Polynomial([3, 5])

        self.assertEqual(p1[3], 5)

        self.assertRaises(ValueError, Polynomial, [])
        self.assertRaises(ValueError, Polynomial, [1])
        self.assertRaises(ValueError, Polynomial, [1, 2, 3])

        p2 = Polynomial([3, 5, 1, 10, 0, 5])

        self.assertEqual(p2[3], 5)
        self.assertEqual(p2[1], 10)
        self.assertEqual(p2[0], 5)

        # String polynomial
        p3 = Polynomial('3 5 1 10 0 5')

        self.assertEqual(p3[3], 5)
        self.assertEqual(p3[1], 10)
        self.assertEqual(p3[0], 5)
