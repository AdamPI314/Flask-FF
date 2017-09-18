# Modified from https://hub.docker.com/r/leafney/ubuntu-mysql/
FROM ubuntu:16.06

# supress warnings such as, debconf: unable to initialize frontend: Dialog ...
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# install openssh-server, openjdk and wget
RUN apt-get -qq update && apt-get -qq install -y openssh-server wget

# install vim, can live without it
RUN apt-get -qq install -y vim
RUN echo "set nu" >> ~/.vimrc 

RUN echo "deb http://cn.archive.ubuntu.com/ubuntu/ xenial main restricted universe multiverse" >> /etc/apt/sources.list

RUN echo "mysql-server mysql-server/root_password password root" | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password root" | debconf-set-selections

RUN apt-get update && \
	apt-get -y install mysql-server-5.7 && \
	mkdir -p /var/lib/mysql && \
	mkdir -p /var/run/mysqld && \
	mkdir -p /var/log/mysql && \
	chown -R mysql:mysql /var/lib/mysql && \
	chown -R mysql:mysql /var/run/mysqld && \
	chown -R mysql:mysql /var/log/mysql

# UTF-8 and bind-address
RUN sed -i -e "$ a [client]\n\n[mysql]\n\n[mysqld]"  /etc/mysql/my.cnf && \
	sed -i -e "s/\(\[client\]\)/\1\ndefault-character-set = utf8/g" /etc/mysql/my.cnf && \
	sed -i -e "s/\(\[mysql\]\)/\1\ndefault-character-set = utf8/g" /etc/mysql/my.cnf && \
	sed -i -e "s/\(\[mysqld\]\)/\1\ninit_connect='SET NAMES utf8'\ncharacter-set-server = utf8\ncollation-server=utf8_unicode_ci\nbind-address = 0.0.0.0/g" /etc/mysql/my.cnf

VOLUME /var/lib/mysql

COPY ./startup.sh /root/startup.sh
RUN chmod +x /root/startup.sh

ENTRYPOINT ["/root/startup.sh"]

EXPOSE 3306

# Use an official Python runtime as a parent image
FROM python:3.5-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 3306 available to the world outside this container
EXPOSE 3306  

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["/usr/bin/mysqld_safe", "python", "app.py"]