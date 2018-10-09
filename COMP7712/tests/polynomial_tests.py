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
        self.assertEqual(Polynomial('7 0 6 2 5 2 3 2 1 1 0 0').degree, 6)

        # Zero polynomial has degree of "None"
        self.assertEqual(Polynomial('1 0 0 0').degree, None)

    def test_iter(self):
        p = Polynomial('13 2 9 5 6 -4 2 1 1 1 0 -2')

        exp = p.degree
        for c in p.coefficients:
            self.assertEqual(p[exp], c)
            exp -= 1

        self.assertEqual(exp, -1)

    def test_str(self):
        p1 = Polynomial([3, 5])
        self.assertEqual(str(p1), '5.0x^3')

        p2 = Polynomial('13 2 9 5 6 -4 2 1 1 1 0 -2')
        self.assertEqual(str(p2), '2.0x^13 + 5.0x^9 - 4.0x^6 + x^2 + x - 2.0')

        p3 = Polynomial('13 2.0 9 5.173 6 -4 0 -0.25')
        self.assertEqual(str(p3), '2.0x^13 + 5.17x^9 - 4.0x^6 - 0.25')

        p4 = Polynomial([1, 1, 0, 1])
        self.assertEqual(str(p4), 'x + 1.0')

        p5 = Polynomial([1, -1, 0, 1])
        self.assertEqual(str(p5), '-x + 1.0')

        p5 = Polynomial([1, 1.0, 0, 1])
        self.assertEqual(str(p5), 'x + 1.0')

        p6 = Polynomial([1, -1.0, 0, 1])
        self.assertEqual(str(p6), '-x + 1.0')

        p7 = Polynomial([1, -1.1, 0, 1.0])
        self.assertEqual(str(p7), '-1.1x + 1.0')

    def test_approx_equal(self):
        # test non-polynomial returns False
        self.assertFalse(Polynomial([1,1]).approx_equal('Not A Polynomial'))

        # test exact match returns true
        p1 = Polynomial([1, 1])
        p2 = Polynomial([1, 1])

        self.assertTrue(p1.approx_equal(p2))

        # test "large difference" returns false
        p1 = Polynomial([1, 1])
        p2 = Polynomial([1, 2])

        self.assertFalse(p1.approx_equal(p2))

        p1 = Polynomial([1, 1])
        p2 = Polynomial([1, 1.000001])

        self.assertTrue(p1.approx_equal(p2, abs_tol=0.00001, rel_tol=1e-50))
        self.assertFalse(p1.approx_equal(p2, abs_tol=0.00000001, rel_tol=1e-50))

        p1 = Polynomial([2, 1.0, 1, 1.0, 0, 1.1])
        p2 = Polynomial([2, 1.001, 1, 1.01, 0, 1.101])

        self.assertTrue(p1.approx_equal(p2, abs_tol=0.011))
        self.assertFalse(p1.approx_equal(p2, abs_tol=0.01))

    def test_get(self):
        p = Polynomial('2 2 1 1 0 0')
        self.assertListEqual([p[2], p[1], p[0]], [2, 1, 0])

        # The coefficient associated with a non-existent term will be returned as 0 for
        # algorithmic convenience
        self.assertEqual(p[p.degree + 1], 0.0)

    def test_set(self):
        p = Polynomial('0 1')

        # Verify that the degree of the polynomial did not change only the
        # coefficient for that term
        orig_degree = p.degree
        p[0] = 2

        self.assertEqual(p.degree, orig_degree)
        self.assertEqual(p[0], 2)

        # Expands the degree of the polynomial
        p = Polynomial('0 1')
        new_degree = 20
        p[new_degree] = 1

        # Verify original term coefficient is still set correctly
        self.assertEqual(p[0], 1)

        # Verify new term's coefficient is set correctly
        self.assertEqual(p[20], 1)

        # Verify that degree of polynomial has been updated
        self.assertEqual(p.degree, new_degree)

        # Verify that the only non-zero coefficients are from the first
        # and the last terms
        self.assertListEqual([p[i] for i in range(1, p.degree)], [0.0] * (p.degree - 1))

    def test_scale(self):
        p = Polynomial('3 1 2 1 1 1')
        self.assertEqual(p.scale(0.0), Polynomial('0 0'))

        p = Polynomial('3 1 2 1 1 1')
        self.assertEqual(p.scale(2.5), Polynomial('3 2.5 2 2.5 1 2.5'))
