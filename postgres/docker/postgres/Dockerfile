FROM       centos:centos6
MAINTAINER Will Ware <wware@veracode.com>

RUN yum update -y
RUN yum localinstall -y http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-centos93-9.3-1.noarch.rpm
RUN yum install -y postgresql93 postgresql93-server postgresql93-contrib sudo vim

ADD image /
RUN chmod +x /usr/bin/postgresql-setup
RUN chmod +x /start_postgres.sh
RUN adduser mobile
RUN /prep_db.sh

EXPOSE 5432

CMD /start_postgres.sh
