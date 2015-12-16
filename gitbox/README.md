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