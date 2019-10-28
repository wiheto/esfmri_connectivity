FROM continuumio/miniconda3:4.7.12
RUN apt-get update && apt-get install -y --no-install-recommends \
	g++=4:8.3.0-1 \
  	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*
RUN pip install pip==19.3.1 
RUN pip install https://github.com/wiheto/fmridenoise@9a858744909e919f61c1942df411aeb30c2190e9
RUN pip install nipype==1.3.0-rc1
ENTRYPOINT /bin/sh
