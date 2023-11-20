from gurobipy import Model, GRB, quicksum
from functions.constraints import create_restrictions_dict
from sets import *
from static_params import *
from dinamic_params import *
from objective_function import create_objective

# for c in range(1, 3):
# 	for h in range(1, (25 - HR_c[c])):
# 		sum = 0
# 		for j in range(h, h + HR_c[c]):
# 			sum +=1
# 		print(quicksum(1 for j in range(h, (h + HR_c[c]))), ' == ', sum)


restriction_list = ['r1.1', 'r1.2', 'r2', 'r4', 'r5.1', 'r5.2', 'r8', 'r9', 'r10', 'r11','r12.3','r13', 'r12.2']
# restriction_list = ['r8', 'r10', 'r9', 'r11']

Camiones = range(1, 72)

def run_model():
	# # Create model
	model = Model("Transicion a camiones eléctricos")

	# Create binary variables
	y_clh = model.addVars(Camiones, EstacionesLenta, Horas, vtype = GRB.BINARY, name = "y_clh")
	x_crh = model.addVars(Camiones, EstacionesRapida, Horas, vtype = GRB.BINARY, name = "x_crh")
	u_lh = model.addVars(EstacionesLenta, Horas, vtype = GRB.BINARY, name = "u_lh")
	v_rh = model.addVars(EstacionesRapida, Horas, vtype = GRB.BINARY, name = "v_rh")
	d_ch = model.addVars(Camiones, Horas, vtype = GRB.BINARY, name = "d_ch")
	t_ch = model.addVars(Camiones, Horas, vtype = GRB.BINARY, name = "t_ch")

	# Create integer variables
	ex_c = model.addVars(Camiones, vtype = GRB.INTEGER, name = "ex_c")
	h_ch = model.addVars(Camiones, Horas, vtype = GRB.INTEGER, name = "h_c")

	# Add variables to model
	model.update()

	# R1: La cantidad de camiones en cada estaci ́on de carga a una hora determinada no puede superar su capacidad maxima
	# R1.1: Estacion lenta
	r1_1 = (quicksum(y_clh[c, l, h] for c in Camiones) <= CTL_l[l] for l in EstacionesLenta for h in Horas)
	# R1.2: Estacion rapida
	r1_2 = (quicksum(x_crh[c, r, h] for c in Camiones) <= CTR_r[r] for r in EstacionesRapida for h in Horas)

	# R2: Un camion no puede estar cargando en dos estaciones a la vez
	r2 = (quicksum(y_clh[c, l, h] for l in EstacionesLenta) + quicksum(x_crh[c, r, h] for r in EstacionesRapida) <= 1 for h in Horas for c in Camiones)

	# R3: Una estacion que esta en reparacion no puede ser utilizada para cargar un camion
	# R3.1: Estacion lenta
	r3_1 = ((y_clh[c, l, h] + u_lh[l, h]) <= 1 for c in Camiones for l in EstacionesLenta for h in Horas)
	# R3.2: Estacion rapida
	r3_2 = ((x_crh[c, r, h] + v_rh[r, h]) <= 1 for c in Camiones for r in EstacionesRapida for h in Horas)

	# R4: Si la cantidad de horas de viaje y carga supera la jornada laboral diaria del conductor se le debe pagar extra
	r4 = (ex_c[c] ==  quicksum((quicksum(y_clh[c, l, h] for l in EstacionesLenta) + 
									quicksum(x_crh[c, r, h] for r in EstacionesRapida)) for h in Horas) + 
									HR_c[c] - J for c in Camiones)

	r5_1 = (quicksum(y_clh[c, l, h] for l in EstacionesLenta) <= 1 - d_ch[c, h] for h in Horas for c in Camiones)
	r5_2 = (quicksum(x_crh[c, r, h] for r in EstacionesRapida) <= 1 - d_ch[c, h] for h in Horas for c in Camiones)

	# R7: Si una estaci ́on alcanza su desgaste maximo debe ser reparada
	# R7.1: Estacion lenta
	r7_1 = (quicksum(y_clh[c, l, h] * DL for h in Horas) <= DLMAX + M * u_lh[l, h] 
					for c in Camiones for l in EstacionesLenta for h in Horas)
	# R7.2: Estacion rapida
	r7_2 = (quicksum(x_crh[c, r, h] * DR for h in Horas) <= DRMAX + M * v_rh[r, h] 
					for c in Camiones for r in EstacionesRapida for h in Horas)

	# R8 Si empieza debe terminar el viaje y no está disponible
	r8 = (t_ch[c, h] * HR_c[c] <= quicksum(d_ch[c, j] for j in range(h, h + HR_c[c]))
						for c in Camiones for h in range(1, 25 - HR_c[c]))
	# R9 Obligar a que realice minimamente una vuelta
	r9 = (quicksum(t_ch[c, h] for h in Horas) == 1 for c in Camiones)

	r10 = (quicksum(d_ch[c, h] for h in Horas) - HR_c[c] == 0 for c in Camiones)

	r11 = (quicksum(t_ch[c, h] for h in range(25 - HR_c[c], 25)) == 0 for c in Camiones)

	r12 = (h_ch[c, h] == (quicksum(quicksum(y_clh[c, l, h] * VCL_c[c] + x_crh[c, r, h] * VCR_c[c] for l in EstacionesLenta for r in EstacionesRapida) - G_c[c] * d_ch[c, h] for h in range(1, h)) / B_c[c]) for h in range(2, 24) for c in Camiones)

	r12_2 = (h_ch[c, h] <= B_c[c] for c in Camiones for h in Horas)

	r12_3 = (h_ch[c, 24] >= 50 for c in Camiones)

	r13 = (h_ch[c, h] >= t_ch[c, h] * HR_c[c] for c in Camiones for h in Horas)

	r14 = ()

	r_mine = {'r1.1': r1_1, 'r1.2': r1_2, 'r2': r2, 'r3.1': r3_1, 'r3.2': r3_2, 'r4': r4, 
						'r7.1': r7_1, 'r7.2': r7_2, 'r5.1': r5_1, 'r5.2': r5_2, 'r8': r8,
						'r9': r9, 'r10': r10, 'r11': r11, 'r12': r12, 'r12.2': r12_2, 'r12.3': r12_3, 'r13': r13}

	# Create restrictions
	r = create_restrictions_dict(y_clh, x_crh, u_lh, v_rh, ex_c)
	for i in restriction_list:
		model.addConstrs(r_mine[i], name = i)

	# Create & add objective function
	objective = quicksum((y_clh[c, l, h] * (CO * VCL_c[c] + CEL) + x_crh[c, r, h] * (CO * VCR_c[c] + CER) 
                                + ex_c[c] * CE + d_ch[c, h]* CC) for l in EstacionesLenta 
                                for r in EstacionesRapida for c in Camiones for h in Horas)
	model.setObjective(objective, GRB.MINIMIZE)

	# Optimize
	model.optimize()
	return model

