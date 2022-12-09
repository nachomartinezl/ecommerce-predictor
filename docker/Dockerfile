FROM python:3.8.13 as base

# Install some packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    vim \
    nano \
    wget \
    curl

# Add a non-root user
RUN useradd -ms /bin/bash app
RUN chown -R app:app /home/app 
USER app

# Setup some paths
ENV PYTHONPATH=/home/app/.local/lib/python3.8/site-packages:/home/app/src
ENV PATH=$PATH:/home/app/.local/bin

# Install the python packages for this new user
ADD requirements.txt .
RUN pip3 install -r requirements.txt
RUN python -m spacy download en_core_web_sm
#RUN pip3 install anytree

WORKDIR /home/app
