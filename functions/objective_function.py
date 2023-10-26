from data.static_params import *
from data.dinamic_params import *
from data.sets import *
from gurobipy import quicksum

def create_objective(x_crh, y_clh, u_lh, v_rh, nc_ch, ex_c):
	# obj = quicksum((y_clh[c, l, h] * (COEL + CCD + CEL) + x_crh[c, r, h] * (COER + CCD + CER) 
	# 							+ v_rh[r, h] * CRER + u_lh[l, h] * CREL + C_e[e] * ex_c[c]) for l in EstacionesLenta 
	# 							for r in EstacionesRapida for c in Camiones for h in Horas for e in E)
	# obj = quicksum(C_e[e] for e in E)
	obj = quicksum((y_clh[c, l, h] * (COEL + CCD + CEL) + x_crh[c, r, h] * (COER + CCD + CER) 
								+ v_rh[r, h] * CRER + u_lh[l, h] * CREL + ex_c[c]) for l in EstacionesLenta 
								for r in EstacionesRapida for c in Camiones for h in Horas for e in E)
	return obj
