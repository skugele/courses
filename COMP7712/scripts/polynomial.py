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
        self._terms = [0.0] * (int(self._spec[0]) + 1)

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

    def approx_equal(self, other, abs_tol=0.0, rel_tol=1e-09):
        if isinstance(other, Polynomial):
            if len(list(self.coefficients)) != len(list(other.coefficients)):
                return False

            for c1, c2 in zip(self.coefficients, other.coefficients):
                if abs(c1 - c2) > max(rel_tol * max(abs(c1), abs(c2)), abs_tol):
                    return False

        return True

    def __len__(self):
        return len(self._terms)

    @property
    def degree(self):
        degree = len(self) - 1

        c = self.coefficients
        while next(c, None) == 0:
            degree -= 1

        return None if degree < 0 else degree

    @property
    def coefficients(self):
        for c in reversed(self._terms):
            yield c
