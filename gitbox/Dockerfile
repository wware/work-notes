FROM ubuntu:14.04
MAINTAINER Sven Dowideit <SvenDowideit@docker.com>

RUN apt-get update -y
RUN apt-get install -y openssh-server python-virtualenv python-pip git ruby
RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

COPY image /

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

RUN useradd -m -d /home/wware -e '' wware
RUN echo 'wware:screencast' | chpasswd
RUN mkdir -p /home/wware/.ssh
RUN echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDFYkkqZ0hcxAgdTB1fI8AmvSujO/vUYn9UVYds7UkSXHWECZHk82j9ob2xwgJs4/zJ41sQOk5PaCGUXtO9BnfZMDNXbHZoyDBFMRpvfT6ASyZsGZ9mN/eqKopLG72IIgJh67a3wl+lhhyQ1hgj0NXmBQsSMq/m976cD5MKuDbjX1gpbLMYoV+e+Ww0UlboTT2Ean0+nHhifP/mJcKlHQV/U6IFvj2EulBBd73UxgugfWA0QOoLE9b4pEr7alQ5nxJc4NZNHiIurE6FX16gFbs31qHRnK4ZhIKflFn+N+TyCCCGt/eygiqzAKHAnQAqDoxgfQ/RCBUDEsIx1dN4QLG5" > /home/wware/.ssh/authorized_keys

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22 1234
CMD ["/bin/bash", "/go.sh"]
