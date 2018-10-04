from functions import poly_divide
from polynomial import Polynomial

# Solution to PA1 (2)
if __name__ == '__main__':
    try:
        p_spec = input('Please specify a polynomial: ')
        p1 = Polynomial(p_spec.split(' '))

        a = float(input('Please provide a number: '))
        p2 = Polynomial([1, 1, 0, -a])

        q, r = poly_divide(p1, p2)
        print('Quotient: {}\nRemainder: {}'.format(q, r))

    except Exception as e:
        print(e)
