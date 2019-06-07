from datetime import datetime
import pandas as pd
import yaml

def ingestdata(): 
	with open('config.yml', 'r') as f:
		config = yaml.safe_load(f)
	return(config)

def clean_table(): 

	#Changed the coloumns in datetime format 
	df = pd.read_csv("./data/raw.csv")
	config = ingestdata()
	df["launched"] = pd.to_datetime( df['launched'] )
	df["deadline"] = pd.to_datetime( df['deadline'] )

	#Calculated duration
	df[ "duration"] = (df["deadline"] - df[ "launched"]).dt.days
	df[ "month_launched"] = df["launched"] .dt.month

	#Created a feature called length of name
	df [ "length_name"] = df["name"].str.len()

	#Data has 6 states: success, cancelled, failed, live, suspended and undefined.
	#Assumed state cancelled is also failed
	#Removed states with live, undefined, suspended as it constitues very small % of data
	df["state"] = df["state"].replace("canceled", "failed")
	df = df[ df["state"] != "live"]
	df = df[ df["state"] != "undefined"]
	df = df[ df["state"] != "suspended"]
	

	#Removed all campaigns 
	threshold_duration = config["load_data"]["duration_delete_value"]
	df = df[(df["duration"] <= threshold_duration) == True]
	df = df.dropna()

	# Dropping coloums we can't use 
	
	list_col_to_delete = config["delete_columns"]
	df = df.drop(list_col_to_delete, axis = 1)


	# State is 
	df[ "state"] = df['state'].apply(lambda x: 1 if x == 'successful'  else 0 )
	df.rename(columns={"main_category_Film & Video": "main_category_Film"}, inplace=True)
	df.to_csv("./clean/cleaned_data.csv", index = False, header= True) 
	



	





