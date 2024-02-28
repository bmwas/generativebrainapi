# generativebrainapi
Code exposes a REST API that runs the Latent Diffusion Model to generate 3D brain scans. Scans are exported to a S3 bucket of choice - except need to generate a .env file with the S3 credentials. 

# Building the Docker Image
docker build -t generativebrainapi .

# Run the docker image (assumes rest endpoint is exposed at port 8000)
docker run -p 8000:8000 generativebrainapi:latest 

