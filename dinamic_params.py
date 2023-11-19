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
B_c = create_dict('bc')
BI_c = create_dict('bi')
HR_c =  create_dict('hr')
VCR_c = create_dict('vcr')
VCL_c = create_dict('vcl')
CTL_l = create_dict('ctl')
CTR_r = create_dict('ctr')
