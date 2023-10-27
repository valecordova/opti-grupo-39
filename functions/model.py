from gurobipy import Model, GRB, quicksum
from functions.constraints import create_restrictions_dict
from data.sets import *
from data.static_params import *
from data.dinamic_params import *
from functions.objective_function import create_objective

restriction_list = ['r1.1', 'r1.2', 'r2', 'r3.1', 'r3.2', 'r4', 'r5.1', 'r5.2', 'r7.1', 'r7.2']

def run_model():
	# Create model
	model = Model("Transicion a camiones eléctricos")

	# Create binary variables
	y_clh = model.addVars(Camiones, EstacionesLenta, Horas, vtype = GRB.BINARY, name = "y_clh")
	x_crh = model.addVars(Camiones, EstacionesRapida, Horas, vtype = GRB.BINARY, name = "x_crh")
	u_lh = model.addVars(EstacionesLenta, Horas, vtype = GRB.BINARY, name = "u_lh")
	v_rh = model.addVars(EstacionesRapida, Horas, vtype = GRB.BINARY, name = "v_rh")

	# Create integer variables
	ex_c = model.addVars(Camiones, vtype = GRB.INTEGER, name = "ex_c")

	# Add variables to model
	model.update()

	# R1: La cantidad de camiones en cada estaci ́on de carga a una hora determinada no puede superar su capacidad maxima
	# R1.1: Estacion lenta
	r1_1 = (quicksum(y_clh[c, l, h] for c in Camiones) <= CTL_l[l] for l in EstacionesLenta for h in Horas)
	# R1.2: Estacion rapida
	r1_2 = (quicksum(x_crh[c, r, h] for c in Camiones) <= CTR_r[r] for r in EstacionesRapida for h in Horas)

	# R2: Un camion no puede estar cargando en dos estaciones a la vez
	r2 = ((y_clh[c, l, h] + x_crh[c, r, h]) <= 1 for c in Camiones for l in EstacionesLenta 
				for r in EstacionesRapida for h in Horas)

	# R3: Una estacion que esta en reparacion no puede ser utilizada para cargar un camion
	# R3.1: Estacion lenta
	r3_1 = ((y_clh[c, l, h] + u_lh[l, h]) <= 1 for c in Camiones for l in EstacionesLenta for h in Horas)
	# R3.2: Estacion rapida
	r3_2 = ((x_crh[c, r, h] + v_rh[r, h]) <= 1 for c in Camiones for r in EstacionesRapida for h in Horas)

	# R4: Si la cantidad de horas de viaje y carga supera la jornada laboral diaria del conductor se le debe pagar extra
	r4 = (quicksum((quicksum(y_clh[c, l, h] for l in EstacionesLenta) + 
									quicksum(x_crh[c, r, h] for r in EstacionesRapida)) for h in Horas) + 
									HR_c[c] <= J + ex_c[c] for c in Camiones)

	# R5: Un camion solo se puede estar cargando si esta disponible a esa hora
	# R5.1: Estacion lenta
	r5_1 = (y_clh[c, l, h] <= D_ch[c, h] for c in Camiones for h in Horas for l in EstacionesLenta)
	# R5.2: Estacion rapida
	r5_2 = (x_crh[c, r, h] <= D_ch[c, h] for c in Camiones for h in Horas for r in EstacionesRapida)

	# R6: El camion debe recuperar la carga gastada durante el d ́ıa
	r6 = (quicksum(y_clh[c, l, h] * VCL_cl[c, l] + x_crh[c, r, h] * VCR_cr[c, r] for h in Horas) 
				>= G_c[c] * HR_c[c] for l in EstacionesLenta for r in EstacionesRapida 
				for c in Camiones)

	# R7: Si una estaci ́on alcanza su desgaste maximo debe ser reparada
	# R7.1: Estacion lenta
	r7_1 = (quicksum(y_clh[c, l, h] * DL for h in Horas) <= DLMAX * M * u_lh[l, h] 
					for c in Camiones for l in EstacionesLenta for h in Horas)
	# R7.2: Estacion rapida
	r7_2 = (quicksum(x_crh[c, r, h] * DR for h in Horas) <= DRMAX * M * v_rh[r, h] 
					for c in Camiones for r in EstacionesRapida for h in Horas)

	r_mine = {'r1.1': r1_1, 'r1.2': r1_2, 'r2': r2, 'r3.1': r3_1, 'r3.2': r3_2, 'r4': r4, 
					'r5.1': r5_1, 'r5.2': r5_2, 'r6': r6, 'r7.1': r7_1, 'r7.2': r7_2}

	# Create restrictions
	r = create_restrictions_dict(y_clh, x_crh, u_lh, v_rh, ex_c)
	for i in restriction_list:
		model.addConstrs(r_mine[i], name = i)

	# Create & add objective function
	objective = create_objective(x_crh, y_clh, u_lh, v_rh, ex_c)
	model.setObjective(objective, GRB.MINIMIZE)

	# Optimize
	model.optimize()
	return model

