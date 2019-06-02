import numpy as np
import sympy as s

"""

Python library for differential equations of various forms

"""
np.seterr(divide='ignore', invalid='ignore')


class Diff:
    """
    Defines the differential equation class
    """

    def __init__(self, expression, degree, variables):
        """
        Initializes the differential class
        :param expression: the definition of the function as an expressed input in terms of (the name scheme)
        :param degree: the degree of the differential equation
        :param variables: tuple of the variables
        """
        if type(degree) != int:
            # Checking for type of degree
            raise TypeError("Dmath Error 10101: Variable 'degree' was %s, not type int." % (str(type(degree))))
        else:
            pass
        self.l = s.lambdify(variables, expression,
                            'numpy')  # Creates a lambda function with inputs (vars) and function (input)
        self.degree = degree
        self.vars = variables

    def Euler(self, init, dx, steps):
        """
        Returns the Euler approximation
        :param init: initial conditions, must be a list of len deg-1
        :param dx: step length (float)
        :param steps: number of steps (int)
        :return: Return nested lists of data [[x],[y],[dy],[ddy],etc.]
        """
        try:
            dxf = float(dx)  # convert dx to float so that there is no rounding error
            data = [[float(p)] for p in init]
            print init
            data.append([self.l(
                    *init)])  # Creates data list of the form [x0],[y0],etc...] #Appends all of the x values to the data
            """
            Main Looping
            """
            try:
                for step in range(1, steps + 1):  # Creates a mapping of values 1-steps in a list
                    # Calculate the next final variable based on the current values in data.
                    data[-1].append(self.l(
                            *[i[-1] for i in data[:-1]]))  # Utilizes all but the last value to construct the next value
                    data[0].append(data[0][-1] + dxf)  # Adds the next x value
                    for variable in range(2, len(data)):
                        # Loops through data excluding the x value and the functional value
                        data[-1 * variable].append(data[-1 * variable][-1] + (data[(-1 * variable) + 1][-1] * dx))
                return data
            except ZeroDivisionError:
                data[-1].append(1000.0)
        except ValueError:
            raise TypeError("Dmath Error 10111: Variable in Diff.Euler was not type int or float.")
        # except TypeError:
        # raise TypeError("Dmath Error 10112: Variable in Diff.Euler was not able to convert to float.")

    def Runge_Kutta(self, initial_conditions, dx, steps):
        """
        Defines the Runge_Kutta estimation of the equation
        :param initial_conditions: Initial Conditions of the method, should be in the form of a nested list
        :param dx: step distance (float)
        :param steps: number of steps (int)
        :return: Data
        """
        init = [initial_conditions[i] for i in range(len(initial_conditions))]  # Converts data format for compatibility
        point_data = init
        if self.degree != 1:
            raise TypeError("Dmath Error 10401: Runge Kutta implementation is limited to first degree ODE.")
        elif (type(dx) != int and type(dx) != float) or type(steps) != int:
            raise TypeError("Dmath Error 10402: Mistyped values: dx must be a float or int, steps must be int.")
        else:
            pass
        for step in range(steps):
            k1 = dx * (self.l(init[0][-1], init[1][-1]))
            k2 = dx * (
                self.l(init[0][-1] + (dx / 2), init[1][-1] + (k1 / 2)))  # Follows k2 = dx(y'(xn + dx/2 , yn + k1/2))
            k3 = dx * (
                self.l(init[0][-1] + (dx / 2), init[1][-1] + (k2 / 2)))  # Follows k3 = dx(y'(xn + dx/2 , yn + k2/2))
            k4 = dx * (self.l(init[0][-1] + (dx / 2), init[1][-1] + k3))
            point_data[1].append(point_data[1][-1] + ((1.0 / 6.0) * (k1 + (2 * k2) + (2 * k3) + k4)))
            point_data[0].append(point_data[0][-1] + dx)
        return point_data

    def Heun(self, init, dx, steps):
        """
                Defines the Heun estimation of the equation
                :param init: Initial points as a nested list [[x],[y]]
                :param dx: step distance (float)
                :param steps: number of steps (int)
                :return: Data
                """
        point_data = init
        if self.degree != 1:
            raise TypeError("Dmath Error 10401: Runge Kutta implementation is limited to first degree ODE.")
        elif (type(dx) != int and type(dx) != float) or type(steps) != int:
            raise TypeError("Dmath Error 10402: Mistyped values: dx must be a float or int, steps must be int.")
        else:
            pass
        for step in range(steps):
            point_data[1].append(point_data[1][-1] +
                                 ((dx / 2.0) * (self.l(point_data[0][-1], point_data[1][-1]) +
                                                self.l(point_data[0][-1] +
                                                       dx, point_data[1][-1] +
                                                       (dx * self.l(point_data[0][-1], point_data[1][-1]))))))
            point_data[0].append(point_data[0][-1] + dx)
        return point_data

    def get_solution_set(self, point_set, euler_settings=(0.1, 100)):
        """
        Returns data from each of the solution sets for the differential
        :param point_set: set including all of the initial points
        :param euler_settings: gives the settings with which to conduct the euler methodology
        :return: data for each of the values
        """
        # Checking length and type of point_set
        output = []
        if len(point_set[0]) != self.degree + 1:
            raise EnvironmentError("Dmath Error 10301: object point_set must have length: %s, not length %s." % (
                str(len(point_set[0])), str(self.degree + 1)))
        elif len(set([len(var) for var in point_set])) != 1:
            raise EnvironmentError("Dmath Error 10302: object 'point_set' must have equal lengths, but does not.")
        else:
            try:
                # Allowing the set to be a float valued array to avoid roundoff errors
                iset = [[float(i) for i in j] for j in point_set]
                for param in range(len(iset)):
                    output.append(self.Euler(iset[param], euler_settings[0], euler_settings[1]))
                return output
            except ValueError:
                raise TypeError("Dmath Error 10303: object 'point_set' must include only float or int type objects.")

    def get_phase_space(self, init, dx=0.1, steps=1000, axis=None, mode='Linear', resolution=100,
                        ind_degree=1, method='Euler'):
        """
        Defines the phase space of the differential equation.
        :param steps: Number of steps with which to construct the approximation
        :param dx: step length
        :param init: initial points
        :param method: type of estimation
        :param ind_degree: degree of derivative to graph
        :param axis: area to graph the phase space, default will graph to necessary area.
        :param mode: Linear or Vector field types
        :param resolution: Resolution of the output space
        :return: Data for the phase space
        """
        if axis is None:
            axis = [-10.0, 10.0, -10.0, 10.0]
        if mode == "Linear":  # Start subprocess as a linear mode
            if method == 'Euler':
                data_constructor = self.Euler(init, dx, steps)
                return [data_constructor[ind_degree], data_constructor[-1]]
            elif method == 'Runge_Kutta' and self.degree == 1:
                data_constructor = self.Runge_Kutta(init, dx, steps)
                return [data_constructor[ind_degree], data_constructor[-1]]
            elif method == 'Heun' and self.degree == 1:
                data_constructor = self.Heun(init, dx, steps)
                return [data_constructor[ind_degree], data_constructor[-1]]
            else:
                raise ValueError(
                        "Dmath Error 10502: Value of the variable 'method' must be 'Euler','Runge_Kutta', or 'Heun'. Not %s." % (
                            str(method)))
        elif mode == 'Vector':  # Returns the phase space in a vector format
            # Creating the Meshgrid
            return False
        else:
            raise ValueError(
                    "Dmath Error 10501: Value of variable 'mode' must be either 'Linear' or 'Vector', not %s" % (
                        str(mode)))

    def get_slope_field(self, axis=None, resolution=100.0):
        """
        Creates the slope field data for the graph
        :param axis: Area to represent
        :param resolution: Number of points to graph the data for
        :return: Returns vector data []
        """
        if axis is None:
            axis = [-10.0, 10.0, -10.0, 10.0]
        # Checking degree type
        if self.degree != 1:
            raise TypeError(
                    "Dmath Error 10501: Slope field cannot generate for degree %s, only for degree 1." % (
                        str(self.degree)))
        # Creating the meshgrid of the "vector" field
        grid_x, grid_y = np.meshgrid(np.arange(axis[0], axis[1], (axis[1] - axis[0]) / resolution),
                                     np.arange(axis[2], axis[3], (axis[3] - axis[2]) / resolution))
        # Generate the data
        try:
            u = 1
            v = self.l(grid_x, grid_y)
            # Normalizing the data
            N = np.hypot(u, v)
            u1, v1 = u / N, v / N
        except RuntimeWarning:
            print N
        return [grid_x, grid_y, u1, v1]



