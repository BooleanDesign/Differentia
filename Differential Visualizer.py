from diff import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import Tkinter as tk

class Application(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Creates the Application wigets
        :return: The wigets that need to be created
        """
        equation_entry = 'Enter Equation Here:'
        diff_label = tk.Label(self,text='Differential Equation: ').grid(row=1,column=1)
        diff_entry = tk.Entry(self,textvariable=equation_entry).grid(row=1,column=2)




    def say_hi(self):
        print("hi there, everyone!")

app = Application()
app.mainloop()


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

