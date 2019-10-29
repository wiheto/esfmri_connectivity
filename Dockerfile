FROM continuumio/miniconda3:4.7.10
RUN apt-get update && apt-get install -y --no-install-recommends \
	g++=4:8.3.0-1 \
	libblas-dev=3.8.0-2 \
	python-dev=2.7.16-1 \
	build-essential=12.6 \
	make=4.2.1-1.2 \
	libigraph0-dev=0.7.1-4 \
	curl=7.64.0-4 \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*
# Installing ANTs 2.2.0 (NeuroDocker build)
ENV ANTSPATH=/usr/lib/ants
RUN mkdir -p $ANTSPATH && \
    curl -sSL "https://dl.dropbox.com/s/2f4sui1z6lcgyek/ANTs-Linux-centos5_x86_64-v2.2.0-0740f91.tar.gz" \
    | tar -xzC $ANTSPATH --strip-components 1
ENV PATH=$ANTSPATH:$PATH
# Python installs
RUN pip install --upgrade pip==19.3.1
RUN pip install bctpy==0.5.0
RUN conda install mkl=2019.4 mkl-service=2.3.0 -y
RUN pip install scikit-learn==0.21.3
RUN pip install pymc3==3.7
RUN pip install matplotlib==3.1.1
RUN pip install plotje==1.1
RUN pip install python-igraph==0.7.0
RUN pip install leidenalg==0.7.0
RUN pip install templateflow==0.4.1
RUN pip install nipype==1.3.0-rc1
RUN pip install nibabel==2.2.
# add user and create a default working directory
WORKDIR /home/esfmri
ENV HOME="/home/esfmri"

