def base36encode(number, alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, (int, long)):
        pass
        raise TypeError('number must be an integer')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36


def hash2(data):
    norm = 2 ** (-32)
    a = 2095533
    s = 0
    c = 1
    t = 0
    t0 = 0
    r = None

    for char in data:
        s = s - ord(char) * 65537 * norm
        if s < 0:
            s = s + 1
        t = a * s + c * norm
        '''
        Since bitwise ops are only defined on integers, floor floats.
        In JS, (0.74 | 93.21) === (0 | 93).
        s = t - (c = int(t) | 0) is syntactically invalid
        '''
        c = int(t) | 0
        t0 = s = t - c
        t = a * s + c * norm
        c = int(t) | 0
        s = t - c

    r = s + t0 * norm
    # Careful : std rep for floats is 6 dec.
    r = int("{0:.16}".format(r)[2:])
    return "{0}".format(base36encode(r))
