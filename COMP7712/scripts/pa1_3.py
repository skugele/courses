# Solution to PA1 (3)
from functions import interpolate

if __name__ == '__main__':
    try:
        coord_list = input('Please specify a set of points: ').split(' ')

        pts = []
        for x, y in zip(coord_list[0::2], coord_list[1::2]):
            pts.append((float(x), float(y)))

        print('Interpolating over points: {{{}}}'.format(','.join(map(lambda x: '({},{})'.format(x[0], x[1]), pts))))

        poly = interpolate(pts)
        print('Resulting Polynomial: ', str(poly))

    except Exception as e:
        print(e)
