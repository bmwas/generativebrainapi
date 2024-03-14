# Generative Brain Inference Endpoint

This code exposes an inference REST API endpoint that runs the Latent Diffusion Model to generate 3D brain scans. Scans are exported to a S3 bucket of choice.  A s3 bucket needs to be created and credentials passed through a .env file (see sample_env.txt). This file also contains the endpoint bearer token or key. 

## Building the Docker Image
To build the image, navigate to the root folder and execute the build command
# docker build -t generativebrainapi .

## Run the docker image (assumes rest endpoint is exposed at port 8000)
To "run" or execute the image (following a successful build above) - execute the following
# docker run -p 8000:8000 generativebrainapi:latest 

## Endpoint access
You can access the endpoint documentation by visiting the server url (e.g. assuming it's localhost) http(s)://localhost:8000/docs

##  Programatically access the API

To programatically call or access the endpoint - see api_inference_example.py attached

