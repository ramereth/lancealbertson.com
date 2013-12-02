Creating a scalable virtualization cluster with Ganeti
######################################################
:date: 2010-05-15 17:39
:author: lance
:tags: cluster, drbd, ganeti, kvm, virtualization, xen, planet
:slug: creating-a-scalable-virtualization-cluster-with-ganeti

Creating a virtualization cluster that is scalable, cheap, and easy to manage
usually doesn't happen in the same sentence. Generally it involves a combination
of a complex set of tools tied together, expensive storage, and difficult to
scale. While I think that the suite of tools that use `libvirt`_ are great and
are headed in the right direction, they're still not quite the right tool for
the right job in some situations. There's also commercial solutions such as
`VMWare`_ and `Xen Server`_ that are great but both cost money (especially if
you want cluster features). If you're looking for a completely open source
solution, then you may have found it.

Enter `Ganeti`_, an open source virtualization management platform created by
Google engineers. I never heard of it until one of the students that works for
me at the `OSUOSL`_ mentioned it while he was being an intern at Google. The
design and goal of Ganeti is to create a virtualization cluster that is stable,
easy to use, and doesn't require expensive hardware.

So what makes it so awesome?

-  A master node controls all instances (virtual machines)
-  Built-in support for `DRBD`_ backed storage on all instances
-  Automated instance (virtual machine) deployment
-  Simple management tools all written in easy to read python
-  Responsive and helpful developer community
-  Works with both Xen and `KVM`_

DRBD
----

The key feature that got me interested was the built-in DRBD support which
enables us to have a "poor man's" SAN using local server storage.  DRBD is
essentially like having RAID1 over the network between two servers. It
duplicates data between two block devices and keeps them in sync. Until
recently, DRBD had to be built as an externel kernel module, but it was recently
added to the mainline kernel in 2.6.33. Ganeti has a seamless DRBD integration
and requires you to have little knowledge in the specific details of setting it
up.

Centralized Instance Management
-------------------------------

Before Ganeti, we had to look up which node an instance was located and it was
difficult to see the whole cluster's state as a whole. During a crisis we would
lose valuable time trying to locate a virtual machine, especially if it had been
moved because of a hardware failure. Ganeti sets one node as a master and
controls the other nodes via remote ssh commands and a restful API. You can
switch which node is the master with one simple command and also recover a
master node if it went offline.  All ganeti commands must run on the master
node.

Ganeti currently uses command line based interactions for all management tasks.
However, it would not be difficult to create a web frontend to manage it. The
OSUOSL actually has a working prototype of a django based web frontend that
we'll eventually release once its out of alpha testing.

Automated Deployment
--------------------

Ganeti uses a set of bash scripts to create an instance on the fly. Each of
these scripts is considered an OS definition and they include a debootstrap
package by default. Since we use several different distributions, I decided to
write my own OS definition using file system dumps instead of direct OS install
scripts. This reduced the deployment time considerably to the point where we can
deploy a new virtual machine in 30 seconds (not counting DRBD sync time). You
can optionally use scripts to setup grub, serial, and networking during the
deployment.

Developer Community
-------------------

The developer community surrounding Ganeti is still quite small but they are
very helpful and responsive. I've sent in several feature and bug requests on
their tracker and usually have a response within 24hrs and even a committed
patch withing 48 hours. The end users on the mailing lists are quite helpful and
usually response quickly as well. Nothing is more important to me in a project
than the health and responsiveness of the community.

OSUOSL use of Ganeti
--------------------

We recently migrated all of our virtual machines to Ganeti using KVM from Xen.
We went from using a 14 blade servers and 3 disk nodes to 4 1U servers with
faster processors, disks, and RAM. We instantly noticed a 2 to 3 times
performance boost in I/O and CPU. A part of boost was the change in the backend
storage, another is KVM.

We currently host around 60 virtual machines total (~15 per node) and can host
up to 90 VMS with our current hardware configuration. Adding an additional node
is a simple task and takes only minutes once all the software is installed. The
new server doesn't need to have the exact same specs however I would recommend
using at least have similar types and speeds of disks and CPUs.

Summary
-------

Ganeti is still young but has matured very quickly over the last year or so. It
may not be the best solution for everyone but it seems to fit quite well at the
OSUOSL. I'll be writing several posts that cover the basics of installing and
using Ganeti. Additionally I'll cover some of the specific steps we took to
deploy our cluster.

.. _libvirt: http://www.libvirt.org
.. _VMWare: http://www.vmware.com
.. _Xen Server: http://www.citrix.com/English/ps2/products/product.asp?contentID=683148&ntref=prod_top
.. _Ganeti: http://code.google.com/p/ganeti/
.. _OSUOSL: http://osuosl.org
.. _DRBD: http://en.wikipedia.org/wiki/DRBD
.. _KVM: http://www.linux-kvm.org/page/Main_Page
