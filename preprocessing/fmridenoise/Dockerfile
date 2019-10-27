FROM continuumio/miniconda3:4.7.12
RUN apt-get update
RUN apt-get install gcc -y
RUN apt-get install libgl1-mesa-glx -y
COPY . ./fmridenoise
RUN pip install pip==19.0.1 
RUN pip install ./fmridenoise/
RUN pip install git+https://github.com/nipy/nipype
ENTRYPOINT /bin/sh
