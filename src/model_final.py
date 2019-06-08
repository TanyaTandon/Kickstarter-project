from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import yaml
from sklearn import metrics
from sklearn.externals import joblib

def ingestdata(): 
	with open('config.yml', 'r') as f:
		config = yaml.load(f)
	return(config)

def fitting():
	config = ingestdata()
	df = pd.read_csv("./clean/cleaned_data.csv")
	y = df ["state"]
	df = df.drop( "state", 1)

	# Encoding category  and main_ category
	df = pd.get_dummies(df, columns = ['category'])
	df = pd.get_dummies(df, columns = ['main_category'])
	df = pd.get_dummies(df, columns = ['currency'])
	df = pd.get_dummies(df, columns=['country'])

	
	ingest_parameters = config["train_model"]["start"]
	seed = ingest_parameters["seed"]
	split_coeff = ingest_parameters[ "split"]


	X_train, X_test, Y_train, Y_test = train_test_split(
		df, y, test_size=  split_coeff, random_state = seed)
	

	params = config["train_model"]["start"]["params"]
	clf = GradientBoostingClassifier(**params)
	FittedModel = clf.fit(X_train, Y_train)

	joblib.dump(FittedModel, "models/GradientBoosting.pkl")
	X_train.to_csv("models/X_train.csv", index = False, header = True)
	X_test.to_csv("models/X_test.csv", index = False, header = True)
	Y_train.to_csv("models/Y_train.csv", index = False, header = True)
	Y_test.to_csv("models/Y_test.csv", index = False, header = True)

	ypred_proba_test =pd.DataFrame(clf.predict_proba(X_test)[:,1])
	ypred_bin_test = pd.DataFrame(clf.predict(X_test)) 
	ypred_proba_test.to_csv("models/ypred_proba_test.csv", index = False,header = True)
	ypred_bin_test.to_csv("models/ypred_bin_test.csv", index = False,header = True)