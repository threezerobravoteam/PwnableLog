#muhe docker study!  
FROM ubuntu:14.04 
MAINTAINER muhe <o0xmuhe@gmail.com> 

COPY ./sources.list /etc/apt/sources.list
RUN apt-get update 
RUN apt-get -y dist-upgrade
RUN apt-get install -y socat 
RUN apt-get install -y openssh-server
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

#ssh-login pre-work
RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]