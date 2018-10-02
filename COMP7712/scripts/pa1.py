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


class Polynomial(object):
    def __init__(self, spec):
        self._spec = spec
        self._terms = []

        if not spec:
            raise ValueError('A polynomial specification must be defined')

        if type(spec) is str:
            self._spec = spec.split()

        if len(self._spec) % 2 != 0:
            raise ValueError('Number of coefficients must match number of exponents')

        # Allocating space for each term
        self._terms = [0] * (int(self._spec[0]) + 1)

        for exp, coeff in zip(self._spec[0::2], self._spec[1::2]):
            self._terms[int(exp)] = float(coeff)

    def __repr__(self):
        return str(self)

    def __str__(self):
        p_terms = []
        for i, c in enumerate(self._terms):
            c = int(c) if float(c) == int(c) else round(c, 2)

            if c == 0:
                continue

            if int(i) == 0:
                term = str(c)

            else:
                c = '' if c == 1 else c

                if int(i) == 1:
                    term = '{}x'.format(str(c))
                else:
                    term = '{}x^{}'.format(str(c), i)

            p_terms.append(term)

        result = ' + '.join(reversed(p_terms))
        result = result.replace(' + -', ' - ')

        return result

    def __getitem__(self, item):
        return self._terms[item]

    def __setitem__(self, key, value):
        self._terms[key] = value

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self._terms == other._terms

        return False

    def __len__(self):
        return len(self._terms)

    @property
    def degree(self):
        return len(self) - 1

    @property
    def coefficients(self):
        for c in reversed(self._terms):
            yield c


if __name__ == '__main__':
    try:
        p_spec = input('Please specify a polynomial: ')
        p1 = Polynomial(p_spec.split(' '))

        a = float(input('Please provide a number: '))
        p2 = Polynomial([1, 1, 0, -a])

        q, r = synthetic_division(p1, p2)
        print('Quotient: {}\nRemainder: {}'.format(q, r))

    except Exception as e:
        print(e)
