import pandas as pd 

def load_data_first():
	df = pd.read_csv("/Users/tanyatandon/desktop/ks-projects-201801.csv")

	df.to_csv("./data/raw.csv", index = False,header = True)
