# Solution to PA1 (3)
if __name__ == '__main__':
    try:
        coord_list = input('Please specify a set of points: ').split(' ')

        pts = []
        for x, y in zip(coord_list[0::2], coord_list[1::2]):
            pts.append((x, y))

        print('Interpolating over points: {{{}}}'.format(','.join(map(lambda x: '({},{})'.format(x[0], x[1]), pts))))

    except Exception as e:
        print(e)
