from sets import *
from random import randint
import pandas as pd
from data_extraction import velocidad_carga_camion

df = pd.read_csv("data/camiones.csv", sep=";")

G_c = {}
VCR_c = {}
VCL_c = {}
HR_c = {}
B_c = {}
BI_c ={}

for c in Camiones:
	tipo = randint(1, 6)
	G_c[c] = float((df.loc[df['id'] == tipo, 'gasto'].item()).replace(",", "."))
	VCR_c[c] = float((df.loc[df['id'] == tipo, 'velocidad carga r1'].item()).replace(",", "."))
	VCL_c[c] = float((df.loc[df['id'] == tipo, 'velocidad carga l1'].item()).replace(",", "."))
	B_c[c] = float((df.loc[df['id'] == tipo, 'capacidad batería'].item()).replace(",", "."))
	HR_c[c] = randint(1, 5)
	BI_c[c] = randint(1, 100)

# G_c = {c: randint(50, 100) for c in Camiones}
# HR_c[c] = {c: randint(1, 6) for c in Camiones}
# VCR_cr = {}
# VCL_cl = {}
# for c in Camiones:
# 	tipo = randint(0, camiones)
# 	VCR_cr[c] = fast[tipo]
# 	VCL_cl[c] = slow[tipo]
# # VCR_cr = {c: fast[randint(0, camiones)] for c in Camiones}
# # VCL_cl = {c: slow[randint(0, camiones)] for c in Camiones}
CTL_l = {l: randint(1, 4) for l in EstacionesLenta}
CTR_r = {r: randint(1, 3) for r in EstacionesRapida}

df = pd.DataFrame.from_dict(G_c, orient='index')
df.to_csv('gc.csv')

df = pd.DataFrame.from_dict(HR_c, orient='index')
df.to_csv('hr.csv')

df = pd.DataFrame.from_dict(B_c, orient='index')
df.to_csv('bc.csv')

df = pd.DataFrame.from_dict(BI_c, orient='index')
df.to_csv('bi.csv')

df = pd.DataFrame.from_dict(VCR_c, orient='index')
df.to_csv('vcr.csv')

df = pd.DataFrame.from_dict(VCL_c, orient='index')
df.to_csv('vcl.csv')

df = pd.DataFrame.from_dict(CTR_r, orient='index')
df.to_csv('ctr.csv')

df = pd.DataFrame.from_dict(CTL_l, orient='index')
df.to_csv('ctl.csv')
