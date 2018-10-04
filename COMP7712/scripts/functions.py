from polynomial import Polynomial


def synthetic_division(p1, p2):
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