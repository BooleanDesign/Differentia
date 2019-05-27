from diff import *
import matplotlib.pyplot as plt


def define_symbols(n, name_scheme=('x', 'numbers')):
    """
    Returns globally defined symbols from sympy with these associated name.
    :param n: Number of variables to define with the method
    :param name_scheme: Way to name the symbols (starting letter, enumerated string type) (str,str)
    :return: True of finished, raises error if failure
    """
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    if n == 1:
        globals()['%s' % name_scheme[0]] = s.Symbol(name_scheme[0])
    elif type(n) == int and name_scheme[1] == 'numbers':
        for j in range(n):
            globals()['%s%s' % (name_scheme[0], str(j + 1))] = s.Symbol(name_scheme[0] + str(j + 1))
        return True
    elif type(n) == int and name_scheme[1] == 'letters':
        for j in range(n):
            globals()['%s%s' % (name_scheme[0], alphabet[j])] = s.Symbol(name_scheme[0] + alphabet[j])
        return True
    else:
        raise ValueError(
                "Dmath Library Error 01101: Function define_symbols failed because n was not int, or because name_scheme was invalid.")
