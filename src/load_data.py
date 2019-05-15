import boto3

s3 = boto3.resource('s3')

copy_source = {'Bucket': 'bossbucket', 'Key': 'ks-projects-201801.csv'}
bucket = s3.Bucket('branchprivatebucket')
bucket.copy(copy_source, 'ks-projects-201801.csv')