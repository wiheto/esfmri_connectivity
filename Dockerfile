FROM continuumio/miniconda3:4.7.10
RUN apt-get update
RUN apt-get install gcc=4:8.3.0-1 -y
RUN apt-get install g++=4:8.3.0-1 -y
RUN apt-get install libblas-dev=3.8.0-2 -y
RUN pip install --upgrade pip==19.2.3
RUN pip install bctpy==0.5.0
RUN conda install mkl=2019.4 mkl-service=2.3.0 -y
RUN pip install scikit-learn==0.21.3
RUN pip install pymc3==3.7
RUN pip install matplotlib==3.1.1
RUN pip install plotje==1.1
ENTRYPOINT /bin/sh
