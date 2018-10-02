from unittest import TestCase

from pa1 import Polynomial, synthetic_division


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

        # Rational coefficients
        p3 = Polynomial('3 0.25 1 10 0 -.105')

        self.assertEqual(p3[3], 0.25)
        self.assertEqual(p3[1], 10)
        self.assertEqual(p3[0], -.105)

    def test_equality(self):
        p1 = Polynomial('10 17 1 2 0 1')
        self.assertEqual(p1, p1)

        self.assertEqual(Polynomial('0 1'), Polynomial('0 1'))
        self.assertEqual(Polynomial('3 4 2 5 1 7'), Polynomial('3 4 2 5 1 7'))
        self.assertEqual(Polynomial('30 3 1 7'), Polynomial('30 3 1 7'))
        self.assertEqual(Polynomial('30 3 1 7'), Polynomial('30 3 1 7'))

        self.assertNotEqual(Polynomial('0 1'), '0 1')

    def test_degree(self):
        self.assertEqual(Polynomial('17 1 6 5 4 2').degree, 17)
        self.assertEqual(Polynomial('0 1').degree, 0)
        self.assertEqual(Polynomial('1 7').degree, 1)
        self.assertEqual(Polynomial('3 -7 2 1 1 19 0 -2').degree, 3)

    def test_iter(self):
        p = Polynomial('13 2 9 5 6 -4 2 1 1 1 0 -2')

        exp = p.degree
        for c in p.coefficients:
            self.assertEqual(p[exp], c)
            exp -= 1

        self.assertEqual(exp, -1)

    def test_str(self):
        p1 = Polynomial([3, 5])
        self.assertEqual(str(p1), '5x^3')

        p2 = Polynomial('13 2 9 5 6 -4 2 1 1 1 0 -2')
        self.assertEqual(str(p2), '2x^13 + 5x^9 - 4x^6 + x^2 + x - 2')

        p3 = Polynomial('13 2.0 9 5.173 6 -4 0 -0.25')
        self.assertEqual(str(p3), '2x^13 + 5.17x^9 - 4x^6 - 0.25')


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

    def test_invalid(self):
        self.assertRaises(ValueError, synthetic_division, Polynomial('1 2'), 2)
        self.assertRaises(ValueError, synthetic_division, 2, Polynomial('1 2'))
        self.assertRaises(ValueError, synthetic_division, 2, 2)

        self.assertRaises(ValueError, synthetic_division, Polynomial('3 5 1 2'), Polynomial('2 1 0 1'))
