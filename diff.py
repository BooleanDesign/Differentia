import sympy as s
import numpy as np
import matplotlib.pyplot as plt
"""

Python library for differential equations of various forms

"""


class diff():
    """
    Defines the differential equation class
    """

    def __init__(self, input, degree,vars):
        """
        Initializes the differential class
        :param input: the definition of the function as an expressed input in terms of (the name scheme)
        :param degree: the degree of the differential equation
        :param vars: tuple of the variables
        """
        if type(degree) != int:
            #Checking for type of degree
            raise TypeError("Dmath Error 10101: Variable 'degree' was %s, not type int." % (str(type(degree))))
        else:
            pass
        self.l = s.lambdify(vars,input, 'numpy') # Creates a lambda function with inputs (vars) and function (input)
        self.degree = degree
        self.vars = vars

    def Euler(self,init,dx,steps):
        """
        Returns the Euler approximation
        :param init: initial conditions, must be a list of len deg-1
        :param dx: step length (float)
        :param steps: number of steps (int)
        :return: Return nested lists of data [[x],[y],[dy],[ddy],etc.]
        """
        try:
            dxf = float(dx) #convert dx to float so that there is no rounding error
            data = [[float(p)] for p in init]
            data.append([self.l(*init)]) #Creates data list of the form [x0],[y0],etc...] #Appends all of the x values to the data
            """
            Main Looping
            """
            for step in range(steps-2):
                error_step_track = step
                for var_id in range(len(data)-2):
                    # Looping over both the steps and the variables within these steps
                    data[-1*(var_id+2)].append(data[-1*(var_id+2)][-1] + (data[-1*(var_id+1)][-1]*dxf))
                data[0].append(data[0][0] + (step * dxf))
                data[-1].append(self.l(*[data[i][-1] for i in range(len(init))]))
            return data
        except ValueError:
            raise TypeError("Dmath Error 10111: Variable in Diff.Euler was not type int or float.")
        except TypeError:
           raise TypeError("Dmath Error 10112: Variable in Diff.Euler was not able to convert to float.")
        except ZeroDivisionError:
            raise SystemError("Dmath Error 10113: Division by 0 encountered at step %s."%(str(error_step_track+1)))

    def Runge_Kutta(self,initial_conditions,dx,steps):
        """
        Defines the Runge_Kutta estimation of the equation
        :param init: Initial points as a nested list [[x],[y]]
        :param dx: step distance (float)
        :param steps: number of steps (int)
        :return: Data
        """
        init = [initial_conditions[i] for i in range(len(initial_conditions))] #Converts data format for compatability
        point_data = init
        if self.degree != 1:
            raise TypeError("Dmath Error 10401: Runge Kutta implementation is limited to first degree ODE.")
        elif (type(dx) != int and type(dx) != float) or type(steps) != int:
            raise TypeError("Dmath Error 10402: Mistyped values: dx must be a float or int, steps must be int.")
        else:
            pass
        for step in range(steps):
            k1 = dx * (self.l(init[0][-1],init[1][-1]))
            k2 = dx * (self.l(init[0][-1] + (dx/2),init[1][-1] + (k1/2))) # Follows k2 = dx(y'(xn + dx/2 , yn + k1/2))
            k3 = dx * (self.l(init[0][-1] + (dx/2),init[1][-1] + (k2/2))) # Follows k3 = dx(y'(xn + dx/2 , yn + k2/2))
            k4 = dx * (self.l(init[0][-1] + (dx/2),init[1][-1] + k3))
            point_data[1].append(point_data[1][-1] + ((1.0/6.0)*(k1+ (2*k2) + (2*k3) + k4)))
            point_data[0].append(point_data[0][-1] + dx)
        return point_data

    def Heun(self,init,dx,steps):
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
                                 ((dx/2.0)*(self.l(point_data[0][-1],point_data[1][-1])+
                                  self.l(point_data[0][-1] +
                                  dx, point_data[1][-1] +
                                  (dx*self.l(point_data[0][-1],point_data[1][-1]))))))
            point_data[0].append(point_data[0][-1] + dx)
        return point_data

    def get_solution_set(self,point_set,euler_settings = (0.1,100)):
        """
        Returns data from each of the solution sets for the differential
        :param point_set: set including all of the initial points
        :param euler_settings: gives the settigns with which to conduct the euler methodology
        :return: data for each of the values
        """
        #Checking length and type of point_set
        output = []
        if len(point_set[0]) != self.degree + 1:
            raise EnvironmentError("Dmath Error 10301: object point_set must have length: %s, not length %s." % (str(len(point_set[0])),str(self.degree+1)))
        elif len(set([len(var) for var in point_set])) != 1:
            raise EnvironmentError("Dmath Error 10302: object 'point_set' must have equal lengths, but does not.")
        else:
            try:
                #Allowing the set to be a float valued array to avoid roundoff errors
                iset = [[float(i) for i in j] for j in point_set]
                for param in range(len(iset)):
                   output.append(self.Euler(iset[param],euler_settings[0],euler_settings[1]))
                return output
            except ValueError:
                raise TypeError("Dmath Error 10303: object 'point_set' must include only float or int type objects.")

    def get_phase_space(self,init,dx=0.1,steps=1000, axis=[-10.0,10.0,-10.0,10.0], mode='Linear', resolution=100, ind_degree=1,method='Euler'):
        """
        Defines the phase space of the differential equation.
        :param axis: area to graph the phase space, default will graph to necessary area.
        :param mode: Linear or Vector field types
        :param resolution: Resolution of the output space
        :return: Data for the phase space
        """
        if mode == "Linear": #Start subprocess as a linear mode
            if method == 'Euler':
                data_constructor = self.Euler(init,dx,steps)
                return [data_constructor[ind_degree],data_constructor[-1]]
            elif method == 'Runge_Kutta' and self.degree == 1:
                data_constructor = self.Runge_Kutta(init,dx,steps)
                return [data_constructor[ind_degree],data_constructor[-1]]
            elif method == 'Heun' and self.degree == 1:
                data_constructor = self.Heun(init,dx,steps)
                return [data_constructor[ind_degree],data_constructor[-1]]
            else:
                raise ValueError("Dmath Error 10502: Value of the variable 'method' must be 'Euler','Runge_Kutta', or 'Heun'. Not %s." %(str(method)))
        elif mode == 'Vector': #Returns the phase space in a vector format
            #Creating the Meshgrid
            phase_x,phase_y = np.meshgrid(np.arange(axis[0],axis[1],resolution),
                                          np.arange(axis[2],axis[3],resolution))
            norm_u = phase_x
        else:
            raise ValueError("Dmath Error 10501: Value of variable 'mode' must be either 'Linear' or 'Vector', not %s" % (str(mode)))



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





y = [1,2,3]
define_symbols(3)
g = diff(-x2,2,(x1,x2,x3))
plt.figure()
r = g.get_phase_space([3.0,0.0,-1.0],method='Euler',ind_degree=2)
c = g.get_phase_space([0.0,4.0,-2.0],method='Euler',ind_degree=2)
p = g.get_phase_space([0.0,1.0,2.0],method='Euler',ind_degree=2)
plt.plot(r[0],r[1])
plt.plot(c[0],c[1])
plt.plot(p[0],p[1])
plt.show()
