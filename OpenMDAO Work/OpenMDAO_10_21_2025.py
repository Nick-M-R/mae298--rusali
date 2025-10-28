# Nicholas Rusali
# 10/21/2025
# MAE 298 - In-Class Activity

# Nicholas Rusali
# MAE 298 
# 10/7/2025

import numpy as np
import openmdao.api as om
from aviary.variable_info.variables import Mission
from cost_externalsubsystem.example_simplecostaviary_variables import Aircraft

# # build the model
# prob = om.Problem()

# prob.model.add_subsystem('paraboloid', om.ExplicitComponent('cost = 10**(3.3191 + 0.8043 * np.log10(MTOW))'))

# # setup the optimization
# prob.driver = om.ScipyOptimizeDriver()
# prob.driver.options['optimizer'] = 'SLSQR' #Type of Optimizer

# prob.model.add_design_var('paraboloid.MTOW', lower=60000, upper=1000000)
# prob.model.add_objective('paraboloid.cost')

# prob.setup()

# # Set initial values.
# prob.set_val('paraboloid.MTOW', 60000.0)


# # run the optimization
# prob.run_driver()

# # Obtaining the results
# print('Optimal MTOW value: ', prob.get_val('paraboloid.MTOW'))
# print('Objective value: ', prob.get_val('paraboloid.cost'))

class SimpleCost(om.ExplicitComponent):
    """
    Component to compute cost based on MTOW.
    """
    def initialize(self):
        self.options.declare('then_year', default=2025, type=int)


    def setup(self):
        # # Inputs
        # self.add_input('MTOW', val=60000.0)  # in pounds
        # self.add_input('t_year', val=2025.0)  # in years

        # # Outputs
        # self.add_output('cost', val=1.0e6)  # in dollars
        self.options.declare(Mission.Summary.MTOW, units='lbm')
        
        self.add_input(Mission.Summary.GROSS_MASS, units='lbm')
        self.add_output(Aircraft.Cost.COST_FLYAWAY, units='USD')
        
        self.declare_partials(of='*', wrt='*', method='fd')

    def compute(self, inputs, outputs):
        MTOW = inputs[Mission.Summary.GROSS_MASS]
        t_year = input['then_year']
        t_year = self.options['then_year']
        
        b_CEF = 5.17053 + 0.104981*(1989-2006)
        
        
        outputs['cost'] = 10**(3.3191 + 0.8043 * np.log10(MTOW))
        
        
# if __name__ == "__main__":
#     # build the model
#     prob = om.Problem()

#     prob.model.add_subsystem('cost_calc', SimpleCost(), promotes_inputs=['MTOW', 't_year'], 
#                              promotes_outputs=['cost'])
    
#     # Sweep MTOW 
#     mtow_values = np.linspace(60000, 1000000, 10)
#     costs = []
#     for mtow in mtow_values:
#         prob.setup()
#         prob.set_val('MTOW', mtow)
#         prob.set_val('then_year', 2025.0)
#         prob.run_model()
#         costs.append(prob.get_val('cost'))
        
#     # Print results
#     for mtow, cost in zip(mtow_values, costs):
#         print(f'MTOW: {mtow:.2f} lbs, Cost: ${cost[0]:.2f}')
    