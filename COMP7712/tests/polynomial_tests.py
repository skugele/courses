from unittest import TestCase

from polynomial import Polynomial


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

    def test_approx_equal(self):
        p1 = Polynomial([1, 1])
        p2 = Polynomial([1, 1])

        self.assertTrue(p1.approx_equal(p2))

        p1 = Polynomial([1, 1])
        p2 = Polynomial([1, 2])

        self.assertFalse(p1.approx_equal(p2))

        p1 = Polynomial([1, 1])
        p2 = Polynomial([1, 1.000001])

        self.assertTrue(p1.approx_equal(p2, abs_tol=0.00001))
        self.assertFalse(p1.approx_equal(p2, abs_tol=0.00000001))

        p1 = Polynomial([2, 1.0, 1, 1.0, 0, 1.1])
        p2 = Polynomial([2, 1.001, 1, 1.01, 0, 1.101])

        self.assertTrue(p1.approx_equal(p2, abs_tol=0.011))
        self.assertFalse(p1.approx_equal(p2, abs_tol=0.01))
