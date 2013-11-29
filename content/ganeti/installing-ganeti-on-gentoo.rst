Installing Ganeti on Gentoo
###########################
:date: 2010-05-21 22:52
:author: lance
:tags: drbd, ganeti, gentoo, kvm, virtualization
:slug: installing-ganeti-on-gentoo

Installing Ganeti is a relatively simple process on Gentoo. This post will go
over the basics on getting it running on Gentoo. Its based primarily on a `wiki
page at the OSUOSL`_ so check it out for more detailed instructions. I also
recommend you read the `upstream docs`_ on Ganeti prior to installing it on your
own. It will cover a lot more topics in detail and this post is intended just as
a diff from that doc.

I should note that I have only installed Ganeti with KVM and have not tested it
with Xen on Gentoo. I appreciate feedback if you have installed and used Xen
with Ganeti on Gentoo. I'm also the current package maintainer for Ganeti and
the related packages in Gentoo such as:

-  `app-emulation/ganeti`_ (primary package)
-  `app-emulation/ganeti-htools`_ (automatic allocation)
-  `app-emulation/ganeti-instance-debootstrap`_ (instance creation)

The first step is to install a base Gentoo system using the standard profile.
You can use a hardened profile however if you intend to use ganeti-htools, it
requires haskell which seems to have issues in hardened.

Configuring DNS
---------------

Ganeti requires the following names to resolve before you can set it up.

-  A master name for the cluster, this IP must be available (ganeti.example.org)
-  A name for each node or Dom0 (node1.example.org)
-  A name for each instance or virtual machine (instance1.example.org)

Kernel
------

`DRBD`_ is optional in Ganeti so you can skip this step if you're not planning
on using it. DRBD was recently included in the mainline kernel in 2.6.33 however
Gentoo's DRBD packages do not currently reflect that.  I hope to get that
changed soon but for now you have two options.

#. Install gentoo-sources, drbd, and drbd-kernel
#. Install gentoo-sources & enable drbd, install drbd without deps

For simplicity, I'll describe option #2 above below. Check out the `wiki page`_
for #1.

DRBD requires you have the following option enabled. Make sure you've rebooted
using a kernel with these options above before you continue.::

    Device Drivers --->
    <*> Connector - unified userspace <-> kernelspace linker

We recommend that you keyword both ``sys-cluster/drbd`` and
``sys-cluster/drbd-kernel`` so that you pull in the latest 8.3.x version.::

    echo "sys-cluster/drbd" >> /etc/portage/package.keywords
    echo "sys-cluster/drbd-kernel" >> /etc/portage/package.keywords

Install DRBD.::

    emerge drbd

Ganeti uses DRBD in a unique way and requires the module to be loaded
with specific settings. Add the autoload settings and load the module.::

    echo "drbd minor_count=255 usermode_helper=/bin/true" >> \
      /etc/modules.autoload.d/kernel-2.6
    modprobe drbd

If you forget this step, you will get an error similar to the one mentioned in
`this email thread`_.

Install Ganeti
--------------

Set the appropriate USE flags. In this case we will be using kvm with drbd.::

    echo "app-emulation/ganeti kvm drbd" >> \
      /etc/portage/package.use

Install Ganeti (you might need to keyword other dependencies)::

    emerge ganeti

Configure Networking
--------------------

There's currently two methods for `setting up networking`_: **bridged** or
**routed.** I picked the bridged method mainly because I'm familiar with the
setup and it seemed to be the simplest.

Ideally you should have a *public* network that will be used for communicating
with the nodes and instances from the outside, and a *backend* private network
that will be used by ganeti for DRBD, migrations, etc. Assuming your *public*
IP (which node1.example.org should resolve to) is 10.1.0.11 and your *backend*
IP is 192.168.1.11, you should edit /etc/conf.d/net to look something like
this:

.. code-block:: bash

    bridge_br0="eth0"
    config_eth0=( "null" )
    config_br0=( "10.1.0.11 netmask 255.255.254.0" )
    routes_br0=( "default gw 10.1.0.1" )

    # make sure eth0 is up before configuring br0
    depend_br0() {
    need net.eth0
    }

    config_eth1=( "192.168.1.11 netmask 255.255.255.0" )

You can have a more complicated networking setup using VLAN tagging and
bridging but I'll go over that in another blog post.

Set the Hostname
----------------

Ganeti is picky about hostnames, and requires that the output of hostname be
fully qualified. So make sure /etc/conf.d/hostname uses the FQDN and looks like
this::

    HOSTNAME="node1.example.org"

**NOT like this:**::

    HOSTNAME="node1"

Configure LVM
-------------

It is recommended that you edit this line in /etc/lvm/lvm.conf::

    filter = [ "r|/dev/nbd.\*|", "a/.\*/", "r|/dev/drbd[0-9]+|"]

The important part is the::

    r|/dev/drbd[0-9]+|

entry, which will prevent LVM from scanning drbd devices.

Now, go ahead and create an LVM volume group with the disks you plan to use for
instance storage. The default name that Ganeti prefers is *xenvg* but we
recommend you choose something more useful for your infrastructure (we use
*ganeti*).::

    pvcreate /dev/sda3
    vgcreate ganeti /dev/sda3

Initialize the Cluster
----------------------

Now we can initialize the cluster on the first node. The command below will do
the following:

-  Set br0 as the primary interface for Ganeti communication
-  Set 192.168.1.11 as the DRBD ip for the node
-  Enable KVM
-  Set the default bridged interface for instances to br0
-  Set the default KVM settings to 2 vcpus & 512M RAM
-  Set the default kernel path to /boot/guest/vmlinuz-x86\_64
-  Set the master DNS name is ganeti.example.org

::

    $ gnt-cluster init --master-netdev=br0 \  
      -g ganeti \  
      -s 192.168.1.11 \  
      --enabled-hypervisors=kvm \  
      -N link=br0 \  
      -B vcpus=2,memory=512M \  
      -H kvm:kernel_path=/boot/guest/vmlinuz-x86_64 \
      ganeti.example.org

Now you have a ganeti cluster! Lets verify everything is setup correctly.::

    $ gnt-cluster verify
    Sun May 16 22:43:00 2010 * Verifying global settings
    Sun May 16 22:43:00 2010 * Gathering data (1 nodes)
    Sun May 16 22:43:02 2010 * Verifying node status
    Sun May 16 22:43:02 2010 * Verifying instance status
    Sun May 16 22:43:02 2010 * Verifying orphan volumes
    Sun May 16 22:43:02 2010 * Verifying remaining instances
    Sun May 16 22:43:02 2010 * Verifying N+1 Memory redundancy
    Sun May 16 22:43:02 2010 * Other Notes
    Sun May 16 22:43:02 2010 * Hooks Results

Yay!

SSH Keys
--------

Ganeti uses ssh to run some tasks but not for all tasks. During the
initialization, it generated a new ssh key for the root user and installs it in
``/root/.ssh/authorized_keys``. In our case, we manage that file with cfengine,
so to work around it we copy the key as ``/root/.ssh/authorized_keys2`` which
ssh will automatically pick up.

Adding nother node
------------------

To add an additional node, you duplicate the setup steps above skipping
initializing the cluster. Instead run the following command::

    gnt-node add -s <node drbd_ip> <node hostname>

Next steps...
-------------

The next steps is actually deploying new virtual machines using Ganeti.  I
wrote a new instance creation script called `ganeti-instance-image`_ which uses
disk images for deployment. I'm currently working on a new project website with
detailed documentation and a blog post about it as well. We're able to deploy
new virtual machines (such as Ubuntu, Centos, or Gentoo) in under 30 seconds
using this method!

.. _wiki page at the OSUOSL: http://dokuwiki.osuosl.org/public/ganeti_cluster_gentoo
.. _upstream docs: http://ganeti-doc.googlecode.com/svn/ganeti-2.1/html/index.html
.. _app-emulation/ganeti: http://packages.gentoo.org/package/app-emulation/ganeti
.. _app-emulation/ganeti-htools: http://packages.gentoo.org/package/app-emulation/ganeti-htools
.. _app-emulation/ganeti-instance-debootstrap: http://packages.gentoo.org/package/app-emulation/ganeti-instance-debootstrap
.. _DRBD: http://www.drbd.org/
.. _wiki page: http://dokuwiki.osuosl.org/public/ganeti_cluster_gentoo
.. _this email thread: http://groups.google.com/group/ganeti/browse_thread/thread/b811f2ba6c898570/f22f4eda4cab62ce
.. _setting up networking: http://ganeti-doc.googlecode.com/svn/ganeti-2.1/html/install.html#configuring-the-network
.. _ganeti-instance-image: http://git.osuosl.org/?p=ganeti-instance-image.git;a=summary
