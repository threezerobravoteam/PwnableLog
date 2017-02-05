#muhe docker study!  
FROM ubuntu:14.04 
MAINTAINER muhe <o0xmuhe@gmail.com> 

COPY ./sources.list /etc/apt/sources.list
RUN apt-get update 
RUN apt-get -y dist-upgrade
RUN apt-get install -y socat 

RUN useradd -m ctf

COPY ./bin/ /home/ctf/
COPY ./start.sh /start.sh

RUN chmod +x /start.sh
RUN chown -R root:ctf /home/ctf
RUN chmod -R 750 /home/ctf
RUN chmod 740 /home/ctf/flag
RUN cp -R /lib* /home/ctf
RUN cp -R /usr/lib* /home/ctf
RUN mkdir /home/ctf/bin
RUN cp /bin/sh /home/ctf/bin
RUN cp /bin/ls /home/ctf/bin
RUN cp /bin/cat /home/ctf/bin

WORKDIR /home/ctf

CMD ["/start.sh"]
EXPOSE 10001