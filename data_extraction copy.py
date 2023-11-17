from datetime import datetime
import pandas as pd
import os

def velocidad_rapida(arr):
	dict_ready = {}
	df = pd.read_excel('camiones_attr/VehicleAttributesFull.xlsx')
	df.drop(df[df['% Electrified'] >= 50].index, inplace = True)
	for camion in arr:
		max_rate = df.loc[df['Vehicle ID'] == camion, 'Max Charge Rate'].values[0]
		dict_ready[camion] = max_rate
	return dict_ready

def velocidad_carga_camion():
	all_files = os.listdir('./camiones_gasto')
	dir_ready = {}

	for file in all_files:
		df = pd.read_csv('./camiones_gasto/' + file)
		head = df.head()
		# format = '%d/%m/%Y %H:%M:%S'
		# format2 = '%m/%d/%Y %H:%M:%S'
		# format3 = '%m/%d/%Y %H:%M'
		# if 'Charging Time' not in head:
		# 	if 'Local Charge E/Time' in head:
		# 			df = df.dropna(axis=0, subset=['Local Charge E/Time'])
		# 			df['Local Charge End Time'] = df['Local Charge E/Time']
		# 	df = df.dropna(axis=0, subset=['Local Charge Start Time'])
		# 	try:
		# 		df['Local Charge End Time'] = pd.to_datetime(df['Local Charge End Time'], format=format)
		# 		df['Local Charge Start Time'] = pd.to_datetime(df['Local Charge Start Time'], format=format)
		# 	except ValueError:
		# 		try:
		# 			df['Local Charge End Time'] = pd.to_datetime(df['Local Charge End Time'], format=format2)
		# 			df['Local Charge Start Time'] = pd.to_datetime(df['Local Charge Start Time'], format=format2)
		# 		except:
		# 			try:
		# 				df['Local Charge End Time'] = pd.to_datetime(df['Local Charge End Time'], format=format3)
		# 				df['Local Charge Start Time'] = pd.to_datetime(df['Local Charge Start Time'], format=format3)
		# 			except:
		# 				break

		# 	df['Charging Time'] = (df['Local Charge End Time'] - df['Local Charge Start Time']).astype('timedelta64[m]')
		
		# 	df = df.dropna(axis=0, subset=['Starting SOC'])
		# 	df = df.dropna(axis=0, subset=['Ending SOC'])
		# 	df['SOC Charged'] = df['Ending SOC'] - df['Starting SOC']

		# df = df.dropna(axis=0, subset=['SOC Charged'])
		# df = df.dropna(axis=0, subset=['Charging Time'])
		# df.drop(df[df['Charging Time'] <= 0].index, inplace = True)
			
		# df['avg_speed'] = df.apply(lambda x: x['SOC Charged'] / (x['Charging Time'] / 60), axis=1)

		dir_ready[df.iloc[0]['Vehicle ID']] = df['Average Power'].mean()
	return dir_ready

keys = velocidad_carga_camion().keys()
print(velocidad_rapida(keys))
print(velocidad_carga_camion())