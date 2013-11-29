Trying out Ganeti with Vagrant
##############################
:date: 2012-05-20 23:09
:author: lance
:tags: ganeti, vagrant, virtualbox, virtualization
:slug: trying-out-ganeti-with-vagrant

`Ganeti`_ is a very powerful tool but often times people have to look for spare
hardware to try it out easily. I also wanted to have a way to easily test new
features of `Ganeti Web Manager (GWM)`_ and `Ganeti Instance Image`_ without
requiring additional hardware. While I do have the convenience of having access
to hardware at the `OSU Open Source Lab`_ to do my testing, I'd rather not
depend on that always. Sometimes I like trying new and crazier things and I'd
rather not break a test cluster all the time. So I decided to see if I could use
`Vagrant`_ as a tool to create a Ganeti test environment on my own workstation
and laptop.

This all started last year while I was preparing for my `OSCON tutorial`_ on
Ganeti and was manually creating VirtualBox VMs to deploy Ganeti nodes for the
tutorial. It worked well but soon after I gave the tutorial I discovered Vagrant
and decided to adapt my OSCON tutorial with Vagrant. Its a bit like the movie
Inception of course, but I was able to successfully get Ganeti working with
Ubuntu and KVM *(technically just qemu)* and mostly functional VMs inside of the
nodes.  I was also able to quickly create a three-node cluster to test failover
with GWM and many facets of the webapp.

The vagrant setup I have has two parts:

#. `Ganeti Tutorial Puppet Module`_
#. `Ganeti Vagrant configs`_

The puppet module I wrote is very basic and isn't really intended for production
use. I plan to re-factor it in the coming months into a completely modular
production ready set of modules. The node boxes are currently running Ubuntu
11.10 (I've been having some minor issues getting 12.04 to work), and the
internal VMs you can deploy are based on the `CirrOS Tiny OS`_. I also created
several branches in the vagrant-ganeti repo for testing various versions of
Ganeti which has helped the GWM team implement better support for 2.5 in the
upcoming release.

To get started using Ganeti with Vagrant, you can do the following::

    git clone git://github.com/ramereth/vagrant-ganeti.git
    git submodule update --init
    gem install vagrant
    vagrant up node1
    vagrant ssh node1
    gnt-cluster verify

Moving forward I plan to implement the following:

-  Update tutorial documentation
-  Support for Xen and LXC
-  Support for CentOS and Debian as the node OS

Please check out the `README`_ for more instructions on how to use the
Vagrant+Ganeti setup. If you have any feature requests please don't hesitate to
create an issue on the github repo.

.. _Ganeti: http://code.google.com/p/ganeti/
.. _Ganeti Web Manager (GWM): https://code.osuosl.org/projects/ganeti-webmgr
.. _Ganeti Instance Image: https://code.osuosl.org/projects/ganeti-image
.. _OSU Open Source Lab: http://osuosl.org
.. _Vagrant: http://vagrantup.com/
.. _OSCON tutorial: http://www.oscon.com/oscon2011/public/schedule/detail/18544
.. _Ganeti Tutorial Puppet Module: https://github.com/ramereth/puppet-ganeti-tutorial
.. _Ganeti Vagrant configs: https://github.com/ramereth/vagrant-ganeti
.. _CirrOS Tiny OS: https://launchpad.net/cirros
.. _README: https://github.com/ramereth/vagrant-ganeti/blob/master/README.md
