import subprocess
from fastapi import FastAPI, HTTPException, Response
import os
import gzip
import boto3
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_nifti_file_to_s3(local_file_path,bucket_name,bucket_folder):
    """
    Uploads a .nii.gz file from local folder to AWS S3 bucket.

    Args:
    local_file_path (str): Local path of the .nii.gz file.
    bucket_name (str): Name of the AWS S3 bucket.
    s3_key_name (str): Key name under which the file will be saved in S3.

    Returns:
    bool: True if upload is successful, False otherwise.
    """   
    try:
        # Initialize S3 client
        # List all files in the folder
        files = os.listdir(local_file_path)
        # Filter only .nii.gz files
        nifti_files = [file for file in files if file.endswith('.nii.gz')]

        # Upload each .nii.gz file to S3 and delete locally
        for file in nifti_files:
            local_file_path = os.path.join(local_file_path, file)
            s3_key_name = os.path.basename(local_file_path)
            try:
                # Upload the file to S3
                s3_key_name = bucket_folder + "/" + str(file)
                print("Attempting to upload file to s3>>>>>>>>>>>>>>>>>>>>>> ")
                s3.upload_file(local_file_path, bucket_name, s3_key_name)
                print(f"File '{file}' uploaded successfully to S3.")
                # Delete the file locally
                os.remove(local_file_path)
            except Exception as e:
                print(f"Error uploading file '{file}' to S3: {e}")
                return False
        print("All files uploaded successfully to S3 and deleted locally.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False    

# Function to read the gzip file
def read_gzip_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def execute_command(config_file,gender, age, ventricular_vol, brain_vol,mriid):
    command = [
        "python", "-m", "monai.bundle", "run", "save_nii",
        "--config_file", config_file,
        "--mriid",str(mriid),
        "--gender", str(gender),
        "--age", str(age),
        "--ventricular_vol", str(ventricular_vol),
        "--brain_vol", str(brain_vol)
    ]
    try:
        result =  subprocess.run(command,capture_output=True,text=True)
        print("Result ====>",result)
        commandresult = {"stdout":str(result)}
    except Exception as e:
        print("Error:", type(e).__name__)
        commandresult = {"stdout":type(e).__name__}
    return commandresult


def generativeexecutecommand(bucket_name,bucket_folder,output_folder,config_file,gender,age,ventricular_vol,brain_vol,mriid):
    print("Attempting a brain generation pipeline ....")
    try:
        result = execute_command(config_file,gender, age, ventricular_vol, brain_vol,mriid) 
        upload_nifti_file_to_s3(output_folder, bucket_name,bucket_folder)
        genoutput = {"results": result}
    except Exception as e:
        print("Error while executing generative model or attemptin s3 upload:", type(e).__name__)
        genoutput = {"results": type(e).__name__}
    return genoutput