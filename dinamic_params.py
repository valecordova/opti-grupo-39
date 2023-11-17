import pandas as pd
from sets import *
from functools import reduce


def create_dict(fileName):
	df = pd.read_csv(f"{fileName}.csv", index_col=0)
	df = df.to_dict("split")
	data = list(reduce(lambda x, y: x + y, df['data'], []))
	df = dict(zip(df["index"], data))
	return df

G_c = create_dict('gc')
HR_c =  create_dict('hr')
VCR_cr = create_dict('vcr')
VCL_cl = create_dict('vcl')
CTL_l = create_dict('ctl')
CTR_r = create_dict('ctr')
HF_ci = {}
for c in Camiones:
	for i in range(1, 24):
		if i + HR_c[c] <= 24:
			HF_ci[c, i] = i + HR_c[c]
		else:
			HF_ci[c, i] = i + 1
