# Use a base image with the desired OS (e.g., Ubuntu, Debian, etc.)
FROM ubuntu:16.04
# Install SSH server

MAINTAINER Hardik Ghoshal <hardik.ghoshal@mailbox.tu-dresden.de>

RUN apt-get update && apt-get upgrade -y

# Install necessary packages
RUN apt-get install -y build-essential libevent-dev libsasl2-dev wget openssh-server sudo libmemcached-tools

# Create an SSH user called ubuntu

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 ubuntu

#RUN useradd -rm -d /home/ubuntu -s /bin/bash -g ubuntu -G sudo -u 1000 ubuntu

RUN echo 'ubuntu:somerandomname' | chpasswd
# Allow SSH access
RUN mkdir /var/run/sshd
# Expose the SSH port
EXPOSE 22


#USER ubuntu

RUN sudo -u ubuntu bash -c "mkdir -p /home/ubuntu/.ssh/ && chmod 700 /home/ubuntu/.ssh"


COPY  ./test_key.pub /home/ubuntu/.ssh/authorized_keys
RUN   cat /home/ubuntu/temp_key.pub >> /home/ubuntu/.ssh/authorized_keys

COPY  ./test_key     /home/ubuntu/.ssh/test_key

USER root

RUN chown -R ubuntu:sudo /home/ubuntu/.ssh/

# Download and build memcached


WORKDIR /home/ubuntu

RUN wget http://memcached.org/files/memcached-1.4.33.tar.gz \
    && tar xzf memcached-1.4.33.tar.gz \
    && cd memcached-1.4.33 \
    && ./configure \
    && make \
    && sudo make install


# Start SSH server on container startup
CMD ["/usr/sbin/sshd", "-D"]

