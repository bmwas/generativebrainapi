"""
Brief script designed to interface with the Brain Generation API, 
requiring essential parameters such as MRI ID, gender, age, 
ventricular volume, and brain volume for processing. 
Additionally, specifications for the destination S3 bucket and folder, 
where NIFTI scans will be deposited, are required. 
The script anticipates input in the form of a CSV file containing 
the aforementioned data points. For reference, an exemplar CSV file
named "example_brain.csv" is included for guidance.

NB: Make sure the endpoint url is complete e.g. /generategenderageventbrainvol

Benson Mwangi @2024
"""

import csv
import requests


def make_api_request(api_url, mriid, gender, age, ventricular_vol, brain_vol, bucket_name, bucket_folder, bearer_token):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + bearer_token,
        "Content-Type": "application/json"
    }
    payload = {
        "mriid": mriid,
        "gender": gender,
        "age": age,
        "ventricular_vol": ventricular_vol,
        "brain_vol": brain_vol,
        "bucket_name": bucket_name,
        "bucket_folder": bucket_folder
    }
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()


# Function to iterate over CSV and make API requests
def process_csv(filename,api_url,bearer_token):
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            mriid = row['mriid']
            gender = float(row['gender'])
            age = float(row['age'])
            ventricular_vol = float(row['ventricular_vol'])
            brain_vol = float(row['brain_vol'])
            bucket_name = row['bucket_name']
            bucket_folder = row['bucket_folder']
            
            # Make API request
            api_response = make_api_request(api_url,mriid, gender, age, ventricular_vol, brain_vol, bucket_name, bucket_folder,bearer_token)           
            # Process API response
            print(api_response)  # You can customize this part to handle the API response as needed
            print("\n")

# Example usage:
bearer_token = "xxxxxxx" # API bearer token or keys - This token is expected to have been pre-populated in the .env file
api_url = "https://localhost.com/generategenderageventbrainvol"
root_dir = "/home/xxxxxxx/"
csv_filename = "sample_inference_file.csv"  # Provide the path to your CSV file
process_csv(root_dir+csv_filename,api_url,bearer_token)
