import gurobipy
import pandas as pd
from dinamic_params import *
import plotly.figure_factory as ff
import networkx as nx
import matplotlib.pyplot as plt

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
		return df

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
	y = create_and_save_table(y, "carga_lenta", ceh)
	x = create_and_save_table(x, "carga_rapida", ceh)
	e = create_and_save_table(e, "horas_extra", c)
	u = create_and_save_table(u, "reparacion_lenta", eh)
	v = create_and_save_table(v, "reparacion_rapida", eh)
	d = create_and_save_table(d, "disponibilidad", ch)
	t = create_and_save_table(t, "inicio_viaje", ch)
	create_gantt(d, y, x)
	create_network_graph(y)

def get_start(hour):
	return (hour - 1)

def create_gantt(df_viaje, df_lenta, df_rapida):
	frames = []
	colors = {'Viajando': 'rgb(238, 96, 85)', 'Lenta': 'rgb(96, 211, 148)', 'Rapida': 'rgb(96, 211, 148)'}
	if df_viaje is not None:
		df_viaje['Start'] =  df_viaje['Hora'].apply(get_start)
		df_viaje['Finish'] = df_viaje['Hora']
		df_viaje['Task'] = df_viaje['Camion']
		df_viaje['Resource'] = "Viajando"
		df_viaje = df_viaje[['Task', 'Start', 'Finish', 'Resource']]
		frames.append(df_viaje)

	if df_lenta is not None:
		df_lenta['Start'] =  df_lenta['Hora'].apply(get_start)
		df_lenta['Finish'] = df_lenta['Hora']
		df_lenta['Task'] = df_lenta['Camion']
		df_lenta['Resource'] = "Lenta"
		df_lenta = df_lenta[['Task', 'Start', 'Finish', 'Resource']]
		frames.append(df_lenta)

	if df_rapida is not None:
		df_rapida['Start'] =  df_rapida['Hora'].apply(get_start)
		df_rapida['Finish'] = df_rapida['Hora']
		df_rapida['Task'] = df_rapida['Camion']
		df_rapida['Resource'] = "Rapida"
		df_rapida = df_rapida[['Task', 'Start', 'Finish', 'Resource']]

	df_total = pd.concat(frames)

	fig = ff.create_gantt(df_total, bar_width= 0.4, group_tasks=True, colors=colors, index_col='Resource')
	fig.update_layout(xaxis_type = 'linear', autosize=False, width=2000, height=2000)
	#['lay']
	fig.show()


def create_network_graph(df_lenta):
	print(df_lenta)
	df_lenta['Estacion'] = df_lenta.apply(lambda x: f"EL {x['Estacion']}", axis = 1)
	df_lenta['Camion'] = df_lenta.apply(lambda x: str(x['Camion']), axis = 1)
	df_lenta['Edge'] = df_lenta.apply(lambda x: (x['Camion'], x['Estacion']), axis = 1)
	df_lenta = df_lenta[df_lenta["Camion"] == 1]
	#df_rapida['Estacion'] = df_rapida['Estacion'].apply(label_rapida)
	#df_total = pd.concat([df_lenta, df_rapida])
	G = nx.DiGraph()
	G.add_nodes_from(df_lenta['Estacion'])
	G.add_nodes_from(df_lenta['Camion'].unique())
	G.add_edges_from(df_lenta['Edge'])
	color_map = []
	for node in G:
		if len(node) > 2:
			if node[:2] == "EL":
				color_map.append('blue')
		else:
			color_map.append('green')
	nx.draw_circular(G, with_labels = True, node_color=color_map)
	plt.savefig("lenta.png")
	

# def create_gantt(df):
# 	data = []
# 	for key in df["Camion"].unique():
# 		df_camion = df.loc[df['Camion'] == key]
# 		min = df_camion['Hora'].min() - 1
# 		max = df_camion['Hora'].max()
# 		data.append(dict(Task=key, Start=min, Finish=max))
# 	df_gantt = pd.DataFrame(data)
# 	print(df_gantt)
# 	fig = ff.create_gantt(df_gantt, bar_width= 0.4)
# 	fig.update_layout(xaxis_type = 'linear', autosize=False, width=2000, height=1500)
# 	fig.show()
