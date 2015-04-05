FROM ubuntu:14.04

RUN apt-get update -y
RUN apt-get -y dist-upgrade
RUN apt-get upgrade -y
RUN apt-get install -yq python-dev python-pip

# Installation:
# Import MongoDB public GPG key AND create a MongoDB list file
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/10gen.list

# Update apt-get sources AND install MongoDB
RUN apt-get update && apt-get install -y mongodb-org

# Create the MongoDB data directory
RUN mkdir -p /data/db

RUN pip install pymongo
RUN pip install jsonschema
#ENTRYPOINT usr/bin/mongod
#CMD usr/bin/mongod
#CMD sudo service mongod start

ADD . /code
WORKDIR /code

RUN pip install -q -e ./

EXPOSE 5000

CMD ["/usr/bin/mongod","python server.py"] 
