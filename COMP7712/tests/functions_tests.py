from unittest import TestCase

from functions import poly_divide, poly_multiply, poly_sum, interpolate
from polynomial import Polynomial


class PolySumTest(TestCase):

    def test_sum(self):
        p1 = Polynomial('0 0')
        p2 = Polynomial('0 1')

        # Test summation with non-zero and zero polynomial
        self.assertEqual(poly_sum(p1, p2), Polynomial('0 1'))

        p1 = Polynomial('1 17')
        p2 = Polynomial('2 12 0 1')

        # Test summation of two non-zero polynomial that have distinct
        # non-zero elements.
        self.assertEqual(poly_sum(p1, p2), Polynomial('2 12 1 17 0 1'))

        # Test summation of two polynomials with non-zero coefficients
        # in all shared terms
        p1 = Polynomial('3 3 2 2 1 1')
        p2 = Polynomial('4 4 3 3 2 2 1 1')
        self.assertEqual(poly_sum(p1, p2), Polynomial('4 4 3 6 2 4 1 2'))


class InterpolateTest(TestCase):
    def test_valid(self):
        self.assertTrue(Polynomial('1 1').approx_equal(interpolate([(1, 1), (2, 2)])))
        self.assertTrue(Polynomial('2 1').approx_equal(interpolate([(-1, 1), (0, 0), (1, 1)])))
        self.assertTrue(Polynomial('3 1').approx_equal(interpolate([(-1, -1), (0, 0), (1, 1), (2, 8)])))
        self.assertTrue(
            Polynomial('3 0.0154 2 -0.8939 1 7.1818 0 -8.9092').approx_equal(
                interpolate([(-1, -17), (3, 5), (2, 2), (50, 8)]), abs_tol=1e-3))

    def test_invalid(self):
        self.assertRaises(ValueError, interpolate, [])
        self.assertRaises(ValueError, interpolate, [(1, 1)])
        self.assertRaises(ValueError, interpolate, [(1, 1), (1, 1)])

        # X values must be distinct
        self.assertRaises(ValueError, interpolate, [(1, 0), (1, 1)])


class PolyMultiplyTest(TestCase):
    def test_valid(self):
        # Testing simple linear polynomials
        p1 = Polynomial('1 1 0 1')
        p2 = Polynomial('1 1 0 1')

        expected = Polynomial('2 1 1 2 0 1')
        actual = poly_multiply(p1, p2)
        self.assertEqual(actual, expected)

        # Testing quadratic multiplied by linear polynomial
        p1 = Polynomial('2 2 0 1')
        p2 = Polynomial('1 1 0 1')

        expected = Polynomial('3 2 2 2 1 1 1 1 0 1')
        actual = poly_multiply(p1, p2)
        self.assertEqual(actual, expected)

        # Testing reverse argument order gives the same result
        actual = poly_multiply(p2, p1)
        self.assertEqual(actual, expected)

        # Testing polynomials with rational coefficients
        p1 = Polynomial('7 3.7 5 2.42 2 2 0 1')
        p2 = Polynomial('2 1.01 1 1 0 1.99')

        expected = Polynomial('9 3.737 8 3.7 7 9.8072 6 2.42 5 4.8158 4 2.02 3 2 2 4.99 1 1 0 1.99')
        actual = poly_multiply(p1, p2)

        self.assertTrue(actual.approx_equal(expected, abs_tol=1e-05))


class PolyDivideTest(TestCase):

    def test_valid(self):
        p1 = Polynomial('1 1 0 1')
        p2 = Polynomial('1 1 0 1')

        q, r = poly_divide(p1, p2)
        self.assertEqual(q, Polynomial('0 1'))
        self.assertEqual(r, 0)

        p1 = Polynomial('4 3 2 7 1 -1 0 3')
        p2 = Polynomial('1 1 0 -1')

        q, r = poly_divide(p1, p2)
        self.assertEqual(q, Polynomial('3 3 2 3 1 10 0 9'))
        self.assertEqual(r, 12)

        p1 = Polynomial('3 1 2 -12 0 -42')
        p2 = Polynomial('1 1 0 -3')

        q, r = poly_divide(p1, p2)
        self.assertEqual(q, Polynomial('2 1 1 -9 0 -27'))
        self.assertEqual(r, -123)

        p1 = Polynomial('5 42 3 -19 0 -13')
        p2 = Polynomial('1 1 0 20')

        q, r = poly_divide(p1, p2)
        self.assertEqual(q, Polynomial('4 42 3 -840 2 16781 1 -335620 0 6712400'))
        self.assertEqual(r, -134248013)

        p1 = Polynomial('3 0.25 2 7.1 0 2.75')
        p2 = Polynomial('1 1 0 1.54')

        q, r = poly_divide(p1, p2)
        self.assertEqual(q, Polynomial('2 0.25 1 6.715 0 -10.3411'))
        self.assertAlmostEqual(r, 18.6753, delta=1e-2)

    def test_invalid(self):
        self.assertRaises(ValueError, poly_divide, Polynomial('1 2'), 2)
        self.assertRaises(ValueError, poly_divide, 2, Polynomial('1 2'))
        self.assertRaises(ValueError, poly_divide, 2, 2)
        self.assertRaises(ValueError, poly_divide, Polynomial('3 5 1 2'), Polynomial('2 1 0 1'))
