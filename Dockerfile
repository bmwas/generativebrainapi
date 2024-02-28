# Use the main version/tag of the miniconda3
FROM continuumio/miniconda3:main

USER root

# Set the working directory to /app
WORKDIR /app
COPY environment.yml /app/environment.yml

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN conda update -n base -c defaults conda && \
    conda env create -f environment.yml && \
    rm -rf /opt/conda/pkgs/*

# Activate the Conda environment
SHELL ["conda", "run", "-n", "monai", "/bin/bash", "-c"]

# Install uvicorn within the Conda environment
RUN conda run -n monai pip install uvicorn

# Copy the current directory contents into the container at /app
ARG CACHEBUST=1
# Set environment variables
ENV NVARCH=x86_64
# Set the working directory back to /app
WORKDIR /app

# Clone MONAI repository
RUN git clone https://github.com/bmwas/MONAI.git
WORKDIR /app/MONAI
# Install MONAI requirements
RUN pip install -r requirements-dev.txt

# Clone GenerativeModels repository
RUN git clone https://github.com/bmwas/MonaiGenerativeModels.git
WORKDIR /app/MONAI/MonaiGenerativeModels
# Install GenerativeModels requirements
RUN pip install -r requirements.txt

# Copy pretrained models
COPY ./models/diffusion_model.pth /app/MONAI/MonaiGenerativeModels/model-zoo/models/brain_image_synthesis_latent_diffusion_model/configs/diffusion_model.pth
COPY ./models/autoencoder.pth /app/MONAI/MonaiGenerativeModels/model-zoo/models/brain_image_synthesis_latent_diffusion_model/configs/autoencoder.pth

# Copy inference JSON file
COPY generategenderageventbrainvol_inference.json /app/MONAI/MonaiGenerativeModels/model-zoo/models/brain_image_synthesis_latent_diffusion_model/configs/generategenderageventbrainvol_inference.json

# Copy all supportive functions over to the functions directory
RUN mkdir /app/MONAI/MonaiGenerativeModels/functions

# Copy generation python code
COPY main.py /app/MONAI/MonaiGenerativeModels/main.py
RUN chmod +x /app/MONAI/MonaiGenerativeModels/main.py


RUN mkdir -p /app/MONAI/MonaiGenerativeModels
COPY ./functions /app/MONAI/MonaiGenerativeModels/functions
RUN chmod +x /app/MONAI/MonaiGenerativeModels/functions/*

# Copy environment file
COPY ./.env /app/MONAI/MonaiGenerativeModels/.env
WORKDIR /app/MONAI/MonaiGenerativeModels

#expose port 8000
EXPOSE 8000

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Define the entry point
CMD ["/bin/bash", "/app/entrypoint.sh"]