from polynomial import Polynomial


def interpolate(pts):
    """
    Calculate an interpolating polynomial for a supplied set of points.

    :param pts: a list of tuples (x,y)
    :return: a polynomial
    """

    # Convert to set to eliminate duplicates
    pts = list(set(pts))

    if len(pts) < 2:
        raise ValueError('Must supply at least 2 distinct points.')

    # Multiply out all terms including (i = j) in lagrange polynomial numerator
    px_all = None
    for pt in pts:
        p = Polynomial([1, 1, 0, -float(pt[0])])
        px_all = p if px_all is None else poly_multiply(px_all, p)

    # Calculate the Lagrange polynomial
    lagrange_poly = Polynomial('0 0')
    for i in range(len(pts)):

        # Divide by (x - x_i).  Remainder must be zero since we constructed px_all
        # from factors that included this divisor
        numerator, _ = poly_divide(px_all, Polynomial([1, 1, 0, -1.0 * float(pts[i][0])]))

        # Denominator is factor of all (x_i - x_j) terms, where i != j
        denominator = 1.0
        for j in range(len(pts)):
            if i != j:
                if pts[i][0] == pts[j][0]:
                    raise ValueError('X coordinate of points must be distinct')
                
                denominator /= (pts[i][0] - pts[j][0])

        px_i = numerator.scale(denominator)

        # Add a_i * px_i to the summation
        lagrange_poly = poly_sum(lagrange_poly, px_i.scale(pts[i][1]))

    return lagrange_poly


def poly_sum(p1, p2):
    """
    Adds the Polynomial arguments and returns the resulting Polynomial.

    :param p1: a Polynomial
    :param p2: a Polynomial
    :return: a Polynomial
    """
    # Result will have degree = max{degree(p1), degree(p2)}

    # If either of the polynomials is the zero polynomial, then
    # short-circuit the sum and just return the other polynomial
    if p1.degree is None:
        return p2
    elif p2.degree is None:
        return p1

    degree = max(p1.degree, p2.degree)
    r = Polynomial('0 0')
    for i in range(degree + 1):
        r[i] += p1[i] + p2[i]

    return r


def poly_multiply(p1, p2):
    """
    Multiplies the Polynomial arguments and returns the resulting Polynomial.

    :param p1: a Polynomial
    :param p2: a Polynomial
    :return: a Polynomial
    """
    # Initialize result polynomial
    r_degree = p1.degree + p2.degree

    r_spec = []
    for i in range(r_degree, -1, -1):
        r_spec.extend([i, 0])

    r = Polynomial(r_spec)

    # Calculate coefficient values for result polynomial
    for i in range(p1.degree + 1):
        for j in range(p2.degree + 1):
            r[i + j] += p1[i] * p2[j]

    return r


def poly_divide(p1, p2):
    """
    Divides an arbitrary degree Polynomial by a linear polynomial, and returns the resulting
     Polynomial quotient and a remainder (if any).

    :param p1: a Polynomial
    :param p2: a linear (degree 1) Polynomial
    :return: a tuple containing a quotient Polynomial and a remainder (as necessary)
    """
    if not (isinstance(p1, Polynomial) and isinstance(p2, Polynomial)):
        raise ValueError('Both arguments must be polynomials')

    if p1 == p2:
        return Polynomial('0 1'), 0

    if p2.degree != 1:
        raise ValueError('Divisor must be degree 1 polynomial')

    if p2[1] != 1:
        raise ValueError('Leading coefficient of divisor must be 1')

    div = -p2[0]
    result = []
    for c in p1.coefficients:
        if len(result) == 0:
            result.append(c)
        else:
            result.append(c + div * result[-1])

    remainder = result.pop()
    poly_spec = []
    for exp, coeff in zip(range(len(result) - 1, -1, -1), result):
        poly_spec.append(exp)
        poly_spec.append(coeff)

    return Polynomial(poly_spec), remainder
