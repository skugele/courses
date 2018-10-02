def synthetic_division(p1, p2):
    pass


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
            self._terms[int(exp)] = int(coeff)

    def __getitem__(self, item):
        return self._terms[item]

    def __setitem__(self, key, value):
        self._terms[key] = value


def run_poly_div():
    p_spec = input('Please specify a polynomial: ')
    p1 = Polynomial(p_spec.split(' '))

    a = input('Please provide a number: ')
    p2 = Polynomial([1, 1, 0, a])


if __name__ == '__main__':
    try:
        run_poly_div()
    except Exception as e:
        print(e)
