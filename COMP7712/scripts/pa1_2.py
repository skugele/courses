from functions import poly_multiply
from polynomial import Polynomial

# Solution to PA1 (2)
if __name__ == '__main__':
    try:
        polynomials = []

        n_list = input('Please specify a list of numbers: ').split(' ')

        for n in n_list:
            polynomials.append(Polynomial([1, 1, 0, -float(n)]))

        print('Computing: ', ''.join(map(lambda p: '({})'.format(str(p)), polynomials)))

        result = None
        for p in polynomials:
            if not result:
                result = p
            else:
                result = poly_multiply(p, result)

        print('Result: ', result)

    except Exception as e:
        print(e)
