
"""
This module contains functions to load the raw data from the source and dump it into the desired location
"""
import os
import logging
import boto3
import config.config as config

from datetime import datetime
import pandas as pd
import yaml


logger = logging.getLogger(__name__)



def clean_table_local(): 

	#Changed the coloumns in datetime format 
	df = pd.read_csv("./data/raw/ks-projects-201801.csv")
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
	df.to_csv("./data/clean/cleaned_data.csv", index = False, header= True) 

def clean_table_AWS(): 
	
	logger.debug("Loading the raw file.")
	
	try:    
		client = boto3.client('s3')
		resource = boto3.resource('s3')
		obj = client.get_object(Bucket=bucket_name, Key=config['load_data']['save_location'] + "/" + config['clean_data']['input_file_name'])
		my_bucket = resource.Bucket(bucket_name)
		df = pd.read_csv(obj['Body'])
	
	except Exception as e:
		logger.error(e)
		return

#Cleaning the data
	logger.debug("Raw file successfully loaded. Starting cleaning process.")
	try:
	
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
		
		df.to_csv(os.path.join(config['clean']['save_location'], config['clean']['output_file_name']))
		my_bucket.upload_file(os.path.join(config['clean']['save_location'], config['clean']['output_file_name']),Key=config['clean']['save_location'] + "/" + config['clean_data']['output_file_name'])
		os.remove(os.path.join(config['clean']['save_location'], config['clean']['output_file_name']))
	

	except Exception as e:
		logger.error(e)
		return



def clean_loading(args):
	'''Fetches the data from the raw source and dumps it at the location specified
	
	Args:
		args: Argparse args - includes args.where, args.manual
		
	Returns:
		None
	'''
	logger.debug('Running the clean_loading function')

	with open(os.path.join("config","config.yml"), "r") as f:
		config = yaml.safe_load(f)
	  
	if args.where == "Local":
		clean_table_local(config)
	
	elif args.where == "AWS":
		clean_table__AWS(config, args.bucket)
			
	else:
			logger.error('Kindly check the arguments and rerun. To understand different arguments, run `python run.py --help`')
			return
	



	





