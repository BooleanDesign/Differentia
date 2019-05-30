from diff import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import Tkinter as tk
import ttk

class Application(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.create_init_widgets()

    def create_init_widgets(self):
        """
        Creates the Application wigets
        :return: The wigets that need to be created
        """
        """
        Widget Variables
        """
        self.selected_estimation_type = tk.StringVar()
        self.equation_entry = tk.StringVar()
        self.del_x = tk.StringVar()
        self.num_step = tk.StringVar()
        self.color = tk.StringVar()
        self.color.set("FFFFFF")
        self.num_step.set("1000")
        self.del_x.set("0.01")
        self.equation_entry.set("Differential Equation")
        self.selected_estimation_type.set("None")
        """
        Section 1
        """
        self.diff_label = tk.Label(self, text='Differential Equation: ').grid(row=1, column=1,sticky='W')
        self.diff_entry = tk.Entry(self, textvariable=self.equation_entry).grid(row=1, column=2,sticky='W')
        self.add_function_button = tk.Button(self, text='Add Equation').grid(row=2, column=2,columnspan=3)
        self.option_label = tk.Label(self, text='Options').grid(row=3, column=1,columnspan=2,sticky="NSWE")
        """
        Section 2
        """
        self.estimation_type = ttk.Combobox(self, textvariable=self.selected_estimation_type)
        self.estimation_type['values'] = ("Euler's Method", "Heun's Method", "Runge Kutta Method")
        self.estimation_type.grid(row=4, column=1)
        """
        Section 2 Label Objects
        """
        self.initial_condition_label = tk.Label(self, text='Initial Conditions').grid(row=4, column=2)
        self.delta_x_label = tk.Label(self, text='Delta X: ').grid(row=5, column=1,sticky="W")
        self.num_step_label = tk.Label(self, text='# of Steps: ').grid(row=6, column=1,sticky="W")
        self.color_label = tk.Label(self, text='Color').grid(row=7, column=1,sticky="W")
        """
        Section 2 Entry Objects
        """
        self.delta_x_entry = tk.Entry(self, textvariable=self.del_x).grid(row=5, column=1,sticky='E')
        self.num_step_entry = tk.Entry(self, textvariable=self.num_step).grid(row=6, column=1,sticky='E')
        self.color_entry = tk.Entry(self, textvariable=self.color).grid(row=7, column=1,sticky='E')
        """
        Section 2 Misc
        """
        self.ini_conds_tree_cols = [("Var", 100), ("Value", 200)]
        self.ini_conds = ttk.Treeview(self,
                                      columns=[col for col, _ in self.ini_conds_tree_cols],
                                      show='headings')
        for col, colwidth in self.ini_conds_tree_cols:
            self.ini_conds.heading(col, text=col.title())
            self.ini_conds.column(col, width=colwidth)
        self.ini_conds.insert('', 'end', text='equ')
        """
        Section 3 Labeling
        """
        self.diffeq_label = tk.Label(self, text='Differential Equations').grid(row=8, column=1,columnspan=2,sticky='NSEW')
        """
        Section 4 Treeview
        """
        self.equ_tracker_tree_cols = [("#", 60), ("Degree", 100), ("Equation", 200), ("Method", 100),
                                      ("Initial Conditions", 100)]
        self.equ_tracker_tree = ttk.Treeview(self,
                                             columns=[col for col, _ in self.equ_tracker_tree_cols],
                                             show='headings')
        for col, colwidth in self.equ_tracker_tree_cols:
            self.equ_tracker_tree.heading(col, text=col.title())
            self.equ_tracker_tree.column(col, width=colwidth)
        """
        Final Gridding
        """
        self.equ_tracker_tree.grid(row=9, column=1,sticky='NSEW',columnspan=2)
        self.ini_conds.grid(row=5, column=2,rowspan=3,sticky='NSEW')
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

