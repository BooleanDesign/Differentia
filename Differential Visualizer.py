import Tkinter as tk
import ttk

import matplotlib
import sympy.parsing.sympy_parser as prs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from diff import *

matplotlib.use("TkAgg")

"""
Error Guide:
1st digit: Class number, 0 if not class
2nd digit: Definition Number 0 if in main code
3rd digit: number of error
4th digit:#
"""


class Application(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.differentials = []
        self.settings = []
        self.pack()
        self.create_init_widgets()
        self.init_plots()


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
        self.degree_entry = tk.StringVar()
        self.initial_conditions_var = tk.StringVar()
        self.color.set("FFFFFF")
        self.num_step.set("1000")
        self.del_x.set("0.01")
        self.equation_entry.set("Differential Equation")
        self.selected_estimation_type.set("None")
        self.initial_conditions_var.set("")
        self.degree_entry.set('1')
        """
        Section 1
        """
        self.deg_label = tk.Label(self, text='Degree: ').grid(row=1, column=1, sticky='W')
        self.deg_entry = tk.Entry(self, textvariable=self.degree_entry).grid(row=1, column=1)
        self.exp_label = tk.Label(self, text='Expression: ').grid(row=1, column=2, sticky='W')
        self.diff_entry = tk.Entry(self, textvariable=self.equation_entry).grid(row=1, column=2)
        self.add_function_button = tk.Button(self, text='Add Equation', command=self.expre_button_func).grid(row=2,
                                                                                                             column=1,
                                                                                                             columnspan=2)
        self.option_label = tk.Label(self, text='Options').grid(row=3, column=1, columnspan=2, sticky="NSWE")
        """
        Section 2
        """
        self.estimation_type_label = tk.Label(self, text='Estimation Type:').grid(row=4, column=1, sticky='W')
        self.estimation_type = ttk.Combobox(self, textvariable=self.selected_estimation_type)
        self.estimation_type['values'] = ("Euler's Method", "Heun's Method", "Runge Kutta Method")
        self.estimation_type.grid(row=4, column=1, sticky='E')
        """
        Section 2 Label Objects
        """
        self.initial_condition_label = tk.Label(self, text='Initial Conditions').grid(row=4, column=2, sticky='W')
        self.delta_x_label = tk.Label(self, text='Delta X: ').grid(row=5, column=1, sticky="W")
        self.num_step_label = tk.Label(self, text='# of Steps: ').grid(row=6, column=1, sticky="W")
        self.color_label = tk.Label(self, text='Color').grid(row=5, column=2, sticky="W")
        """
        Section 2 Entry Objects
        """
        self.initial_condition_entry = tk.Entry(self, textvariable=self.initial_conditions_var).grid(row=4, column=2,
                                                                                                     sticky='E')
        self.delta_x_entry = tk.Entry(self, textvariable=self.del_x).grid(row=5, column=1, sticky='E')
        self.num_step_entry = tk.Entry(self, textvariable=self.num_step).grid(row=6, column=1, sticky='E')
        self.color_entry = tk.Entry(self, textvariable=self.color).grid(row=5, column=2, sticky='E')
        """
        Section 3 Labeling
        """
        self.diffeq_label = tk.Label(self, text='Differential Equations').grid(row=8, column=1, columnspan=2,
                                                                               sticky='NSEW')
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
        self.equ_tracker_tree.grid(row=9, column=1, sticky='NSEW', columnspan=2)
        """
        Menu Bar
        """
        self.gui_menu = tk.Menu(self.master)  # Creates the overarching gui menu
        self.master.config(menu=self.gui_menu)
        # Creating the submenus
        self.filemenu = tk.Menu(self.gui_menu)
        self.editmenu = tk.Menu(self.gui_menu)
        self.helpmenu = tk.Menu(self.gui_menu)
        self.settingsmenu = tk.Menu(self.gui_menu)
        # creating the cascades
        self.gui_menu.add_cascade(label='File', menu=self.filemenu)
        self.gui_menu.add_cascade(label='Edit', menu=self.editmenu)
        self.gui_menu.add_cascade(label='Help', menu=self.helpmenu)
        self.gui_menu.add_cascade(label='Settings', menu=self.settingsmenu)
        """
        Creating the Filemenu
        """
        self.filemenu.add_command(label='Open', command=self.client_open)
        self.filemenu.add_command(label='Save As', command=self.client_save)
        self.filemenu.add_command(label='Import Data', command=self.client_import)
        self.filemenu.add_command(label='Export Data', command=self.client_export)
        self.filemenu.add_command(label='Print Graphs', command=self.client_printgraphs)
        self.filemenu.add_command(label='Exit', command=self.client_exit)
        """
        Creating the Editmenu
        """
        """
        Creating the Help Menu
        """
        """
        Creating the Settings Menu
        """
        self.settingsmenu.add_command(label='Change Settings', command=self.settings_frame)

    def init_plots(self):
        """
        Initiates the plots
        :return:
        """
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.ax1 = self.figure.add_subplot(111)
        self.graph_canvas = (FigureCanvasTkAgg(self.figure, self))
        self.graph_canvas.show()
        self.graph_canvas.get_tk_widget().grid(row=1, column=3, rowspan=9, sticky='NSEW')

    def settings_frame(self):
        return False

    def client_save(self):
        return False

    def client_printgraphs(self):
        return False

    def client_export(self):
        return False

    def client_import(self):
        return False

    def client_open(self):
        return False

    def client_exit(self):
        exit()

    def add_function(self):
        """
        Adds the function to the function list
        :return:
        """
        # Checking the var length
        self.var_exp = prs.parse_expr(self.equation_entry.get())
        self.expression = parse_function(self.equation_entry.get())
        if len(self.initial_conditions_var.get().split(',')) != int(self.degree_entry.get()) + 1:
            raise IndexError()
        else:
            pass
        # Addings the settings to the set
        self.settings.append(([float(i) for i in self.initial_conditions_var.get().split(',')],
                              self.selected_estimation_type.get(),
                              float(self.del_x.get()),
                              int(self.num_step.get()),
                              self.color.get()))
        self.differentials.append(Diff(self.expression, int(self.degree_entry.get()), list(self.var_exp.free_symbols)))

    def update_graph(self):
        """
        Adds the graph data to the graphs
        :return:
        """
        self.ax1.cla()
        for expression_id in range(len(self.differentials)):
            # Looping through each of the data
            print self.settings
            data = self.differentials[expression_id].Euler(self.settings[expression_id][0],
                                                           self.settings[expression_id][2],
                                                           self.settings[expression_id][3])
            self.ax1.plot(data[0], data[-1])
        self.graph_canvas.show()

    def expre_button_func(self):
        self.add_function()
        self.update_graph()




def parse_function(expr):
    """
    Parses through a (str) type object to form a functional lambda expression
    :param expr: The expression to be parsed <str>
    :return: Returns the lambda type function
    """
    """
    Start by checking the variable forms of the equation. Should have x followed by y1,y2,y3, etc.
    y1 = dy/dx, y2 = d2y/dx2, etc...
    """
    ex = prs.parse_expr(expr)
    syms_in_exp = [str(i) for i in list(prs.parse_expr(expr).free_symbols)]
    print syms_in_exp, type(syms_in_exp)
    # Checking the name of the various symbols
    if False in [('y' in i or i == 'x') for i in syms_in_exp]:
        " One of the variables is not correct"
        raise ValueError("Differentia Error 0101: Symbol of input must be 'x' or 'yn', not %s" % str(
            syms_in_exp[[('y' in i or i == 'x') for i in syms_in_exp].index(False)]))
    else:
        # Cleared the name check, now trying to lambdify
        try:
            # Must create a symbol for each of the symbols in the expression, as such,
            define_symbols(1, ('x', 'numbers'))
            define_symbols(len(syms_in_exp) - 1, ('y', 'numbers'))
            return prs.parse_expr(expr)
        except SyntaxError:
            raise ValueError("Differentia Error 0102: Syntax of the expression was wrong.")

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


app = Application()
app.mainloop()
