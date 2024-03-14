"""
Brief script designed to interface with the Brain Generation API, 
requiring essential parameters such as MRI ID, gender, age, 
ventricular volume, and brain volume for processing. 
Additionally, specifications for the destination S3 bucket and folder, 
where NIFTI scans will be deposited, are required. 
The script anticipates input in the form of a CSV file containing 
the aforementioned data points. For reference, an exemplar CSV file
named "example_brain.csv" is included for guidance.

Benson Mwangi @2024
"""

import csv
import requests

# Function to make API request
def make_api_request(api_url,mriid, gender, age, ventricular_vol, brain_vol, bucket_name, bucket_folder):
    payload = {
        "mriid": mriid,
        "gender": gender,
        "age": age,
        "ventricular_vol": ventricular_vol,
        "brain_vol": brain_vol,
        "bucket_name": bucket_name,
        "bucket_folder": bucket_folder
    }
    response = requests.post(api_url, json=payload)
    return response.json()

# Function to iterate over CSV and make API requests
def process_csv(filename,api_url):
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
            api_response = make_api_request(api_url,mriid, gender, age, ventricular_vol, brain_vol, bucket_name, bucket_folder)
            
            # Process API response
            print(api_response)  # You can customize this part to handle the API response as needed

# Example usage:
api_url = "YOUR_API_URL_HERE"
root_dir = "/home/Benson/Dropbox/Antillegence/MVP_Development/Seed_Database_and_Crawling/welnity_apis/langchain/monai/inference/generativebrainapi/"
csv_filename = "sample_inference_file.csv"  # Provide the path to your CSV file
process_csv(root_dir+csv_filename)
