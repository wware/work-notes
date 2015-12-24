Gitbox, a private mobile Github clone
=====================================

This is a hardware project to assist software development. The hardware comprises:

* A Raspberry Pi model B+
* A 1-terabyte USB hard drive, or maybe instead a USB stick
  - 128 GB USB stick for $28 - http://www.amazon.com/SanDisk-Ultra-128GB-Flash-SDCZ43-128G-G46/dp/B00YFI1EBC
* A 16x2 LCD display for showing the IP address and hostname
* A backup battery, MOSFET, boost converter, and Arduino Pico (or equivalent)
* Maybe a nice case? http://www.adafruit.com/products/1985

Here is what it looks like with a USB stick. But this scenario does not have a friendly Github-like UI.

* http://www.instructables.com/id/GitPi-A-Private-Git-Server-on-Raspberry-Pi/
* http://thomasloughlin.com/gitpi-using-your-raspberry-pi-as-a-dedicated-git-repository/
* http://monkeyhacks.com/post/raspberry-pi-as-private-git-server

The Raspberry Pi could run Gitlab

* https://sjugge.be/blog/resource/raspberry-pi-git-and-ci-server-gitlab
* https://gitlab.maikel.pro/maikeldus/WhatsSpy-Public/wikis/getting-started-rpi-image
* https://about.gitlab.com/downloads/#raspberrypi2
* http://www.instructables.com/id/GitPi-A-Private-Git-Server-on-Raspberry-Pi/

or Gogs

* http://blog.meinside.pe.kr/Gogs-on-Raspberry-Pi/
* http://javaguirre.net/2014/11/09/hosting-private-git-repositories-in-a-raspberry-pi/
* https://www.atavendale.co.uk/2015/03/installing-gogs-on-a-raspberry-pi/
* https://gogs.io/

The backup battery, MOSFET, boost converter and Arduino have the job of
detecting that the power cord has been pulled, supplying auxiliary power,
telling the RPi to shut down, detecting when shutdown has finished, and
switching off the auxiliary power. There should be a LED that stays lit until
the power is really off, maybe the RPi has one of its own.

Gitlab via Docker
====

Begin by installing Docker on your Linux VM. The docker.io package in the
standard Ubuntu repository is too old and busted and crappy.

```
$ curl -sSL https://get.docker.com/ | sh
$ sudo usermod -a -G docker $USER
```

You'll need to log out and log back in for the second command to take effect.

Put this line in the file `/etc/default/docker`.

```
DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4 --bip=192.168.0.1/24"
```

Then type:

```
sudo service service docker restart
docker pull gitlab/gitlab-ce
sudo docker run --detach \
    --hostname gitlab.example.com \
    --publish 8443:443 --publish 8080:80 --publish 2222:22 \
    --name gitlab \
    --restart always \
    --volume /srv/gitlab/config:/etc/gitlab \
    --volume /srv/gitlab/logs:/var/log/gitlab \
    --volume /srv/gitlab/data:/var/opt/gitlab \
    gitlab/gitlab-ce:latest
```

After starting the instance, I needed to use "git exec -it gitlab /bin/bash" to go
in and change the file /etc/gitlab/gitlab.rb, changing the value of "unicorn[list]"
to "0.0.0.0". Then I could reach the webserver onn port 8080 of the docker host.
Tthe root password is initially "5iveL!ve" and they'll want you to immediately change
it to something else.
