from .sets import *
from random import randint

G_ch = {(c, h): randint(1, 20) for c in Camiones for h in Horas}
CTL_l = {l: randint(1, 20) for l in EstacionesLenta}
CTR_r = {r: randint(1, 20) for r in EstacionesRapida}
NC_c1 = {(c, 1): randint(1, 20) for c in Camiones}
CMAX_c = {c: randint(10, 20) for c in Camiones}
VCR_cr = {(c, r): randint(1, 10) for c in Camiones for r in EstacionesRapida}
VCL_cl = {(c, l): randint(1, 10) for c in Camiones for l in EstacionesLenta}
HR_c = {c: randint(0, 11) for c in Camiones}
D_ch = {(c, h): randint(0, 1) for c in Camiones for h in Horas}
# Como funciona esta? por donde tiene que recorrer e?
# C_e = {(e): randint(10, 100) for e in Horas}
