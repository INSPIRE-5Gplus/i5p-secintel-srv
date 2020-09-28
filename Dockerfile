FROM python:3-slim
RUN apt-get update -qqy && \
	apt-get -qqy install wget g++ && \
	rm -rf /var/lib/apt/lists/*
# show python logs as they occur
ENV PYTHONUNBUFFERED=0

# get packages
WORKDIR /
COPY requirements.in requirements.in
RUN python3 -m pip install pip-tools
RUN pip-compile --output-file=requirements.txt requirements.in
RUN python3 -m pip install -r requirements.txt

# add files into working directory
COPY logger.py .
COPY secintel.py .

# set listen port
ENV PORT_HTTP "8181"
EXPOSE 8181


ENTRYPOINT ["python", "/secintel.py"]
