from .sets import *
from random import randint

G_c = {c: randint(1, 20) for c in Camiones}
CTL_l = {l: randint(1, 10) for l in EstacionesLenta}
CTR_r = {r: randint(1, 10) for r in EstacionesRapida}
VCR_cr = {(c, r): randint(1, 10) for c in Camiones for r in EstacionesRapida}
VCL_cl = {(c, l): randint(1, 10) for c in Camiones for l in EstacionesLenta}
HR_c = {c: randint(2, 11) for c in Camiones}
D_ch = {(c, h): randint(0, 1) for c in Camiones for h in Horas}
