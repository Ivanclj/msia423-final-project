
import argparse
import boto3
s3 = boto3.client("s3")

def download_data(args):
	"""read the data from the data source
	Args:
		args (str): strings entered from the commend. 

	Returns:
		df (:py:class:`pandas.DataFrame`): Dowloaded csv file. 
	"""
	s3.download_file(args.bucket, args.filename, args.savename)

if __name__ == "__main__":
	#download data from the source
	parser = argparse.ArgumentParser(description="Download data from S3")

	parser.add_argument("--bucket", help="Target S3 bucket name")
	parser.add_argument("--filename", help="Target file want to dowlaod")
	parser.add_argument("--savename", help="Filename to be save")

	args = parser.parse_args()
	download_data(args)