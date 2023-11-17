from model import run_model
from result import get_active_vars

result_files = [ "out.json", "out.lp", "out.rlp", "out.mps", "out.mst", 
								"out.sol", "out.hnt", "out.prm", "out.attr"]

def write_results(m):
	for i in result_files:
		m.write("results/" + i)
	m.printAttr("ObjVal")

def main():
	m = run_model()
	write_results(m)
	
	get_active_vars(m)

if __name__ == "__main__":
	main()
