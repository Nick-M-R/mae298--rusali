# Nicholas Rusali
# MAE 298 
# 10/8/2025

import openmdao.api as om

# build the model
prob = om.Problem()
exec = om.ExecComp(['z = x**2 + y','f = (x-4)**2 + x*y + (y+3)**2 - 3'])

prob.model.add_subsystem('paraboloid', exec)

# setup the optimization
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP' #Type of Optimizer

prob.model.add_design_var('paraboloid.x', lower=-50, upper=50)
prob.model.add_design_var('paraboloid.y', lower=-50, upper=50)
prob.model.add_objective('paraboloid.f')
# Add constraints
prob.model.add_constraint('paraboloid.z', lower=1.0, upper=8.0)

prob.setup()

# Set initial values.
prob.set_val('paraboloid.x', 3.0)
prob.set_val('paraboloid.y', -4.0)



# run the optimization
prob.run_driver()

# Obtaining the results
print('Optimal x value: ', prob.get_val('paraboloid.x'))
print('Optimal y value: ', prob.get_val('paraboloid.y'))
print('Objective value: ', prob.get_val('paraboloid.f'))

# def f(x,y):
#     f = (x-4)**2 + x*y + (y+3)**2 - 3
#     return f

# print('f(-1,7) =',f(-1,7))