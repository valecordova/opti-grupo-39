from datetime import datetime
import pandas as pd
import os

def velocidad_carga_camion():
	all_files = os.listdir('./camiones_gasto')
	slow_ready = {}
	fast_ready = {}
	df = pd.read_excel('camiones_attr/VehicleAttributesFull.xlsx')
	df.drop(df[df['% Electrified'] >= 50].index, inplace = True)
	i = 0
	for file in all_files:
		df2 = pd.read_csv('./camiones_gasto/' + file)
		camion = df2.iloc[0]['Vehicle ID']
		capacity = df.loc[df['Vehicle ID'] == camion, 'Rated Energy'].values[0]
		slow = capacity // df2['Average Power'].mean()
		fast = capacity // df.loc[df['Vehicle ID'] == camion, 'Max Charge Rate'].values[0]
		if slow > 0 and fast > 0 and slow < 20 and fast < 90:
			slow_ready[i] = slow
			fast_ready[i] = fast
			i += 1
	return [slow_ready, fast_ready]
