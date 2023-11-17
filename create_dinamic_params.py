from sets import *
from random import randint
import pandas as pd
from data_extraction import velocidad_carga_camion

velocidades = velocidad_carga_camion()

camiones = len(velocidades[0].keys()) - 1

slow = velocidades[0]
fast = velocidades[1]

G_c = {c: randint(50, 100) for c in Camiones}
HR_c =  {}
HF_ci = {}
for c in Camiones:
	random = randint(5, 8)
	HR_c[c] = random
	HF_ci[c] = {i: i + random if i + random <= 24 else i + 1 for i in range(1, 24)}
VCR_cr = {}
VCL_cl = {}
for c in Camiones:
	tipo = randint(0, camiones)
	VCR_cr[c] = fast[tipo]
	VCL_cl[c] = slow[tipo]
# VCR_cr = {c: fast[randint(0, camiones)] for c in Camiones}
# VCL_cl = {c: slow[randint(0, camiones)] for c in Camiones}
CTL_l = {l: randint(1, 4) for l in EstacionesLenta}
CTR_r = {r: randint(1, 3) for r in EstacionesRapida}

df = pd.DataFrame.from_dict(G_c, orient='index')
df.to_csv('gc.csv')

df = pd.DataFrame.from_dict(HR_c, orient='index')
df.to_csv('hr.csv')

df = pd.DataFrame.from_dict(HF_ci, orient='index')
df.to_csv('hf.csv')

df = pd.DataFrame.from_dict(VCR_cr, orient='index')
df.to_csv('vcr.csv')

df = pd.DataFrame.from_dict(VCL_cl, orient='index')
df.to_csv('vcl.csv')

df = pd.DataFrame.from_dict(CTR_r, orient='index')
df.to_csv('ctr.csv')

df = pd.DataFrame.from_dict(CTL_l, orient='index')
df.to_csv('ctl.csv')
