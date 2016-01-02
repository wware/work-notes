Gitbox, a private mobile Github clone
=====================================

This is a hardware project to assist software development. The hardware comprises:

* A Raspberry Pi model B+
* A 1-terabyte USB hard drive, or maybe instead a USB stick
  - 128 GB USB stick for $28 - http://www.amazon.com/SanDisk-Ultra-128GB-Flash-SDCZ43-128G-G46/dp/B00YFI1EBC
* A 16x2 LCD display for showing the IP address and hostname
* A backup battery, MOSFET, boost converter, and Arduino Pico (or equivalent)
* Maybe a nice case? http://www.adafruit.com/products/1985

The backup battery, MOSFET, boost converter and Arduino have the job of
detecting that the power cord has been pulled, supplying auxiliary power,
telling the RPi to shut down, detecting when shutdown has finished, and
switching off the auxiliary power. There should be a LED that stays lit until
the power is really off, maybe the RPi has one of its own.

I spent some time playing with both Gitlab and Gogs, and ultimately
settled upon a vanilla
[Git server](https://git-scm.com/book/en/v1/Git-on-the-Server) using
[GitWeb](https://git.wiki.kernel.org/index.php/Gitweb) as a web interface.
The web interface appears on port 1234.

```bash
docker build -t gitbox .
docker run -d -v /opt/git:/opt/git --name=gitbox gitbox
docker inspect gitbox | grep IPAddress
```

It's a good idea to put an entry for "gitbox" in `/etc/hosts`.

Creating a git repo is a bit of a chore. Given a repository foo, do this.

```bash
git clone --bare foo foo.git
scp -r foo.git gitbox:/opt/git/foo.git
```
