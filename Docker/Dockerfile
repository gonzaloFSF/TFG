FROM ubuntu

RUN apt-get update -y
RUN apt-get install openssh-server -y
RUN apt-get install strace -y
RUN apt-get install apache2 -y
RUN apt-get install git -y
RUN apt-get install python3.7 -y
RUN apt-get install python3-pip -y
RUN pip3 install Django==3.0.3
RUN a2enmod rewrite
RUN a2enmod proxy
RUN a2enmod proxy_http
RUN a2enmod proxy_balancer
RUN a2enmod lbmethod_byrequests

RUN mkdir /root/.ssh

COPY ./start.sh /bin/start.sh
COPY ./authorized_keys /root/.ssh
COPY ./known_hosts /root/.ssh/
COPY ./id_rsa /root/.ssh/
COPY ./id_rsa.pub /root/.ssh/
COPY ./config /root/.ssh/
COPY ./apache_django.conf /etc/apache2/conf-enabled/

CMD /bin/start.sh

