import re


class Polynomial(object):
    """
    A class for representing arbitrary real coefficient polynomials
    """

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
        for i, c in enumerate(map(lambda x: round(x, 2), self._terms)):

            if c == 0:
                continue

            if int(i) == 0:
                term = str(c)

            else:

                if int(i) == 1:
                    term = '{}x'.format(str(c))
                else:
                    term = '{}x^{}'.format(str(c), i)

            p_terms.append(term)

        result = ' + '.join(reversed(p_terms))
        result = result.replace(' + -', ' - ')
        result = re.sub(r'(-?)(\D?)1.0x', r'\1\2x', result)

        return result

    def __getitem__(self, key):
        return self._terms[key] if key < len(self) else 0.0

    def __setitem__(self, key, value):

        # Automatically expand the number of terms if necessary.  This
        # will not change the degree of the polynomial unless the added
        # term is non-zero
        if key >= len(self):
            self._terms.extend([0.0] * (key - len(self) + 1))

        self._terms[key] = value

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            return False

        if self.degree != other.degree:
            return False

        if self.degree is None:
            return True

        for i in range(0, self.degree + 1):
            if self[i] != other[i]:
                return False

        return True

    def approx_equal(self, o, abs_tol=1e-09, rel_tol=1e-06):
        if not isinstance(o, Polynomial):
            return False

        for i in range(max(self.degree, o.degree) + 1):
            abs_diff = abs(self[i] - o[i])
            rel_threshold = rel_tol * max(abs(self[i]), abs(o[i]))
            if abs_diff > max(rel_threshold, abs_tol):
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

    def scale(self, scalar):
        self._terms = [c * scalar for c in self._terms]
        return self
