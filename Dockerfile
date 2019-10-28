FROM continuumio/miniconda3:4.7.10
RUN apt-get update && apt-get install -y --no-install-recommends \
	g++=4:8.3.0-1 \
	libblas-dev=3.8.0-2 \
	python-dev=2.7.16-1 \
	build-essential=12.6 \
	make=4.2.1-1.2 \
	libigraph0-dev=0.7.1-4 \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip==19.2.3
RUN pip install bctpy==0.5.0
RUN conda install mkl=2019.4 mkl-service=2.3.0 -y
RUN pip install scikit-learn==0.21.3
RUN pip install pymc3==3.7
RUN pip install matplotlib==3.1.1
RUN pip install plotje==1.1
RUN pip install python-igraph==0.7.0
RUN pip install leidenalg==0.7.0
ENTRYPOINT /bin/sh
