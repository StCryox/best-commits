FROM  bde2020/spark-master:3.2.0-hadoop3.2

RUN apk update && apk add make automake gcc g++ gfortran subversion python3-dev && pip3 install numpy
