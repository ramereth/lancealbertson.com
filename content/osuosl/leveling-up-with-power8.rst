Leveling up with POWER8
#######################
:date: 2015-08-04 13:37
:author: lance
:tags: ibm, power8
:slug: leveling-up-with-power8
:status: draft

Over the past year I've had the privilege of working on a new POWER architecture
ppc64le (PowerPC 64bit Little Endian). We've had a long relationship with IBM at
the Open Source Lab (OSL) providing resources for the POWER architecture to FOSS
projects.

Earlier this year, IBM graciously donated three powerful POWER8 machines to the
OSL to replace our aging FTP cluster. This produced a few challenges we needed
to overcome to make this work:

* We're primarily an x86 shop, so we needed to get used to the POWER8 platform
  in a production environment
* This platform is extremely new, so we're on the leading edge using this
  hardware in a production environment
* It was recommended to use the new ppc64le architecture by the IBM engineers,
  which was still getting support from RedHat at the time
* There was no CentOS ppc64le build yet and RHEL 7 wasn't quite officially
  supported yet (however, it was added in 7.1)
* This platform uses a different boot process than other machines, namely the
  OPAL firmware which uses the Petitboot boot loader

POWER8 architecture differences
-------------------------------

We've been using IBM POWER7 hardware for many years which requires the use of a
proprietary management system called the Hardware Management Console (HMC). It
was an extremely difficult system to use and was so foreign to how we normally
manage systems. So when we got our first POWER8 system, I was delighted to see
that they did away with the HMC and provided an abstraction layer called OPAL to
manage the system. Basically, it meant these machines actually use open
standards and essentially boot like an x86 machine more or less (i.e. what we're
more used to).

When you first boot a POWER8 machine that is using OPAL, you use IPMI to connect
to the serial console (which needs to be enabled in the FSP). The FSP stands for
the Flexible Service Processor which is basically the low level firmware that
manages the hardware of the machine. When it first boots up, you'll see a Linux
kernel booting up and then a boot prompt running Petitboot. Petitboot is a
kexec based boot loader.

This basically allows you to do the following:

* Auto-boots a kernel
* Gives you a bash prompt to diagnose the machine or setup hardware RAID
* Give you a sensible way to install an OS remotely

When it boots an installed system, it'll actually do a kexec and reboot into the
actual OS kernel. Overall, it is an easy and simple way to remotely manage a
machine.

Operating System Setup
----------------------

The next major challenge was creating a stable operating system environment.
When I first started to test these machines, I was using a beta build of RHEL 7
for ppc64le that contained bugs. Thankfully 7.1 was released recently which
provided a much more stable installer and platform in general. Getting the OS
installed was the easy part, the more challenging part was getting our normal
base system up with Chef. This required manually building a chef client for
ppc64le since none existed yet. We ended up building the client using the
Omnibus Chef build on a guest which meant we had to bootstrap the build
environment some a little too.

The next challenge was installing all of the base packages and packages we
needed for running our FTP mirrors. Most of those packages are in EPEL however
there is no ppc64le builds (yet) for the architecture. So we needed up having to
build many of the dependencies using mock and hosting it in a local
repository. Thankfully we didn't require many dependencies, and all of the
builds had no compile problems.

Storage layout and configuration
--------------------------------

One of the other interesting parts of this was the storage configuration for the
servers. These machines came with five 387GB SSDs and ten 1.2TB SAS disks.  The
hardware RAID controller comes with a feature called RAID6T2 which provides a
two tier RAID solution but visible as a single block device. Essentially it uses
the SAS disks for the cold storage and the SSDs are for hot cache access and
writing.

Being a lover of open source, I was interested in seeing how this performed
against other technologies such as bcache. While I don't have all of the numbers
still, the hardware RAID out performed bcache by quite a bit. Eventually I'd
like to see if there are other tweaks so we aren't reliant on a proprietary RAID
controller, but for now the controller is working flawlessly.

Production deployment and results
---------------------------------

We successfully deployed all three new POWER8 servers without any issue on June
18, 2015. We're already seeing a large increase in utilization on the new
machines as they have far more I/O capacity and throughput than the previous
cluster. I've been extremely impressed with how stable and how fast these
machines are.

Since we're on the leading edge of using these machines, I'm hoping to write
more detailed and technical blog posts on the various steps I went through.
