# Use a base image with the desired OS (e.g., Ubuntu, Debian, etc.)
FROM ubuntu:16.04
# Install SSH server

MAINTAINER Hardik Ghoshal <hardik.ghoshal@mailbox.tu-dresden.de>

# Install necessary packages
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y openssh-server sudo

# Add user 

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 ubuntu

RUN echo 'ubuntu:somerandomname' | chpasswd
# Allow SSH access
RUN mkdir /var/run/sshd

# Expose the SSH port

EXPOSE 22


#USER ubuntu

RUN mkdir -p /home/ubuntu/.ssh/

COPY  ./test_key.pub /home/ubuntu/.ssh/authorized_keys
COPY  ./test_key 	 /home/ubuntu/.ssh/test_key
RUN   cat /home/ubuntu/temp_key.pub >> /home/ubuntu/.ssh/authorized_keys

USER root

RUN chown -R ubuntu:sudo /home/ubuntu/.ssh/


# Install other packages
RUN apt-get install -y build-essential libevent-dev libsasl2-dev wget libmemcached-tools git r-base

# Create an SSH user called ubuntu


# clone and install dude

#USER ubuntu

WORKDIR /home/ubuntu

COPY Benchmark.py /home/ubuntu/Benchmark.py
COPY Dudefile /home/ubuntu/Dudefile
COPY graphs.R /home/ubuntu/graphs.R
COPY run.sh /home/ubuntu/run.sh
RUN chmod 777 /home/ubuntu/run.sh


RUN git clone https://bitbucket.org/db7/dude \
	&& cd dude \
	&& python setup.py install


RUN wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/twemperf/mcperf-0.1.1.tar.gz \
	&& tar xzf mcperf-0.1.1.tar.gz \
	&& cd mcperf-0.1.1 \
	&& ./configure \
	&& make \
	&& sudo make install


# Start SSH server on container startup
CMD ["/usr/sbin/sshd", "-D"]

