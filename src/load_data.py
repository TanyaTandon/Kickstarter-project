import boto3

def load_data(args): 
	s3 = boto3.resource('s3')
	bucketname = args.bucket

	copy_source = {'Bucket': 'bossbucket', 'Key': 'ks-projects-201801.csv'}
	bucket = s3.Bucket(bucketname)
	bucket.copy(copy_source, 'ks-projects-201801.csv')