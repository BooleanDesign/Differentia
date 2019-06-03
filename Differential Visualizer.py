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
        self.add_function_button = tk.Button(self, text='Add Equation', command=self.update_graphs).grid(row=2,
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

    def update_graphs(self):
        """
        Updates the GUI graphs and inputs newly entered data
        :return: True if passed
        """
        # Add current data
        self.differentials.append(self.create_expression(self.equation_entry.get(), int(self.degree_entry.get())))
        # Generate Settings
        self.settings.append(([float(i) for i in self.initial_conditions_var.get().split(',')],
                              float(self.del_x.get()),
                              int(self.num_step.get()),
                              self.color.get(),
                              self.selected_estimation_type.get()))
        # Populating the Treeview
        self.equ_tracker_tree.insert("", "end", "",
                                     values=(str(len(self.differentials)),
                                             str(self.differentials[-1].degree),
                                             str(self.equation_entry.get()),
                                             str(self.selected_estimation_type.get()),
                                             str(self.settings[-1][0][1:-1])))
        # Clear the graphs that already exist. They are defined in self.ax1 in init_plots()
        self.ax1.cla()
        for expression in range(len(self.differentials)):
            # Looping through each of the expressions in the current list of expressions. Each type is type Diff
            exp_data = self.differentials[expression].est_dict[self.selected_estimation_type.get()](
                self.settings[expression][0],
                                                            self.settings[expression][1],
                self.settings[expression][2])  # Must be in form [inits],float(dx),int(steps)
            self.ax1.plot(exp_data[0], exp_data[1], color='#' + self.color.get())
        self.graph_canvas.show()
        # Resetting all of the variables
        self.equation_entry.set("")
        self.initial_conditions_var.set("")

    def create_expression(self, exp, degree):
        """
        Creates an expression of type __main__.class.Diff()
        :param exp: expression of type <str>
        :param degree: degree of the expression as an int
        :return: Return expression of type __main.class.Diff()
        """
        # Checking if expression args are correct types
        if type(exp) != str:
            raise TypeError("Differentia Error 1501: Type of arg_name: exp must be str, not %s" % (str(type(exp))))
        elif type(degree) != int:
            raise TypeError(
                "Differentia Error 1502: Type of arg_name: degree must be int, not %s" % (str(type(degree))))
        else:
            pass
        try:
            generated_expression = prs.parse_expr(exp)  # This is the working expression of the function
            generated_degree = int(degree)
            # Creating the correct variables
            generated_vars = define_symbols(degree)
            return Diff(generated_expression, generated_degree, generated_vars)
        except SyntaxError:
            raise SyntaxError("Differentia Error 1503: Syntax of user entry (%s) could not be parsed." % (str(exp)))

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


def define_symbols(degree):
    """
    Defines the symbols needed for sympy
    :param degree: degree of symbols needed
    :return: tuple of these global variables
    """

    if int(degree) > 0:
        globals()['x'] = s.Symbol('x')
        for j in range(degree):
            globals()['y%s' % (str(j + 1))] = s.Symbol('y%s' % (str(j+1)))
    else:
        raise ValueError("Differentia Error 0101: Arg: degree entry failed, %s !> 0" % (str(degree)))
    return tuple([globals()['x']] + [globals()['y%s' % (i)] for i in range(1, degree+1)])





app = Application()
app.mainloop()
