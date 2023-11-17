import gurobipy
import pandas as pd
import matplotlib.pyplot as plt
from dinamic_params import *

def extract_from_var(var, value, amount):
	result = []
	splitted = var.split("[")[1]
	first = splitted.split("]")[0]
	if amount == 1:
		result.append(int(first))
	elif amount >= 2:
		splitted = first.split(",")
		result.append(int(splitted[0]))
		result.append(int(splitted[1]))
		if amount == 3:
			result.append(int(splitted[2]))
	result.append(int(value))
	return result

def create_and_save_table(dict, fileName, columns):
	if len(dict) > 0:
		df = pd.DataFrame.from_dict(dict, orient='index')
		df.columns = columns
		df.to_excel(f"results/{fileName}.xlsx", index=False)
		df.to_csv(f"results/{fileName}.csv")

def get_active_vars(model: gurobipy.Model):
	x = {}
	y = {}
	e = {}
	u = {}
	v = {}
	t = {}
	d = {}
	ceh = ["Camion", "Estacion", "Hora", "Valor"]
	ch = ["Camion", "Hora", "Valor"]
	eh = ["Estacion", "Hora", "Valor"]
	c = ["Camion", "Valor"]
	for var in model.getVars():
		if var.varName.startswith("x") and var.x > 0 and var.x is not None:
			x[str(var.varName)] = extract_from_var(str(var.varName), var.x, 3)
		elif var.varName.startswith("y") and var.x > 0 and var.x is not None:
			y[str(var.varName)] = extract_from_var(str(var.varName), var.x, 3)
		elif var.varName.startswith("e") and var.x > 0 and var.x is not None:
			e[str(var.varName)] = extract_from_var(str(var.varName), var.x, 1)
		elif var.varName.startswith("u") and var.x > 0 and var.x is not None:
			u[str(var.varName)] = extract_from_var(str(var.varName), var.x, 2)
		elif var.varName.startswith("v") and var.x > 0 and var.x is not None:
			v[str(var.varName)] = extract_from_var(str(var.varName), var.x, 2)
		elif var.varName.startswith("d") and var.x > 0 and var.x is not None:
			d[str(var.varName)] = extract_from_var(str(var.varName), var.x, 2)
		elif var.varName.startswith("t") and var.x > 0 and var.x is not None:
			t[str(var.varName)] = extract_from_var(str(var.varName), var.x, 2)
		else:
			pass
	create_and_save_table(y, "carga_lenta", ceh)
	create_and_save_table(x, "carga_rapida", ceh)
	create_and_save_table(e, "horas_extra", c)
	create_and_save_table(u, "reparacion_lenta", eh)
	create_and_save_table(v, "reparacion_rapida", eh)
	create_and_save_table(d, "disponibilidad", ch)
	create_and_save_table(t, "inicio_viaje", ch)
