from gurobipy import Model, GRB
from functions.constraints import create_restrictions_dict
from data.sets import *
from functions.objective_function import create_objective

restriction_list = ['r1.1', 'r1.2', 'r2', 'r3.1', 'r3.2', 'r4', 'r5.1', 'r5.2', 'r6', 'r7.1', 'r7.2']

def run_model():
	# Create model
	model = Model("Transicion a camiones eléctricos")

	# Create binary variables
	y_clh = model.addVars(Camiones, EstacionesLenta, Horas, vtype = GRB.BINARY, name = "y_clh")
	x_crh = model.addVars(Camiones, EstacionesRapida, Horas, vtype = GRB.BINARY, name = "x_crh")
	u_lh = model.addVars(EstacionesLenta, Horas, vtype = GRB.BINARY, name = "u_lh")
	v_rh = model.addVars(EstacionesRapida, Horas, vtype = GRB.BINARY, name = "v_rh")

	# Create integer variables
	nc_ch = model.addVars(Camiones, Horas, vtype = GRB.INTEGER, name = "nc_ch")
	ex_c = model.addVars(Camiones, vtype = GRB.INTEGER, name = "ex_c")

	# Add variables to model
	model.update()

	# Create restrictions
	r = create_restrictions_dict(y_clh, x_crh, u_lh, v_rh, nc_ch, ex_c)
	for i in restriction_list:
		model.addConstrs(r[i], name = i)

	# Create & add objective function
	objective = create_objective(x_crh, y_clh, u_lh, v_rh, nc_ch, ex_c)
	model.setObjective(objective, GRB.MINIMIZE)

	# Optimize
	model.optimize()
