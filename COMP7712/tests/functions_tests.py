from unittest import TestCase

from functions import synthetic_division
from polynomial import Polynomial


class SyntheticDivisionTest(TestCase):

    def test_valid(self):
        p1 = Polynomial('1 1 0 1')
        p2 = Polynomial('1 1 0 1')

        q, r = synthetic_division(p1, p2)
        self.assertEqual(q, Polynomial('0 1'))
        self.assertEqual(r, 0)

        p1 = Polynomial('4 3 2 7 1 -1 0 3')
        p2 = Polynomial('1 1 0 -1')

        q, r = synthetic_division(p1, p2)
        self.assertEqual(q, Polynomial('3 3 2 3 1 10 0 9'))
        self.assertEqual(r, 12)

        p1 = Polynomial('3 1 2 -12 0 -42')
        p2 = Polynomial('1 1 0 -3')

        q, r = synthetic_division(p1, p2)
        self.assertEqual(q, Polynomial('2 1 1 -9 0 -27'))
        self.assertEqual(r, -123)

        p1 = Polynomial('5 42 3 -19 0 -13')
        p2 = Polynomial('1 1 0 20')

        q, r = synthetic_division(p1, p2)
        self.assertEqual(q, Polynomial('4 42 3 -840 2 16781 1 -335620 0 6712400'))
        self.assertEqual(r, -134248013)

        p1 = Polynomial('3 0.25 2 7.1 0 2.75')
        p2 = Polynomial('1 1 0 1.54')

        q, r = synthetic_division(p1, p2)
        self.assertEqual(q, Polynomial('2 0.25 1 6.715 0 -10.3411'))
        self.assertAlmostEqual(r, 18.6753, delta=1e-2)

    def test_invalid(self):
        self.assertRaises(ValueError, synthetic_division, Polynomial('1 2'), 2)
        self.assertRaises(ValueError, synthetic_division, 2, Polynomial('1 2'))
        self.assertRaises(ValueError, synthetic_division, 2, 2)

        self.assertRaises(ValueError, synthetic_division, Polynomial('3 5 1 2'), Polynomial('2 1 0 1'))
