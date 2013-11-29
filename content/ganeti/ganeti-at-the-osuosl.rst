Ganeti at the OSUOSL
####################
:date: 2010-12-08 23:34
:author: lance
:tags: django, ganeti, kvm, virtualization
:slug: ganeti-at-the-osuosl

One of the many large projects I'm working on at the `OSUOSL`_ has been
migrating all of our virtualization over to `Ganeti`_ and `KVM`_.  Needless to
say its kept me from updating my blog but I hope to make up for it. I thought I
would give a rundown of how we use Ganeti at the OSUOSL and where we plan to
move forward from there.

So far we have 10 clusters ranging in size from single nodes up to 4 node
clusters. Each node is running Gentoo and managed with our cfengine setup. There
are approximately 120 virtual machines deployed across all the clusters with the
majority (~70) in our production cluster of four nodes. Each node in the
production cluster is running between 17 to 18 KVM instances.

Project Ganeti Clusters
-----------------------

Several hosted projects including `OSGeo`_, `phpBB`_, and `ECF`_ have their own
clusters which we fully manage on the node level. It works well for them as they
don't have to worry about maintaining the virtualization cluster while giving
them the flexibility of deploying dedicated VMs on their own hardware. I've been
recommending moving towards this direction for current projects and new projects
we get requests for. So far it seems to be working well for both the OSUOSL and
the projects we host.

Image Deployment
----------------

For deployment we use `ganeti-instance-image`_ which is something I wrote to
help make deployments faster and more flexible. It uses various types of images
(tarball, filesystem dump, qemu-img) to unpack a pre-made system and deploy it
with networking, grub, and serial fully functional. Creating the images is
currently a manual process but I have it semi-automated using kickstart and
preseed config files for building systems quickly and predictably. The amazing
part is deploying a fully functional VM in under one minute using
ganeti-instance-image.

Web-based Management
--------------------

An upcoming tool that the OSUOSL is working on is a web-based frontend for
managing Ganeti clusters called `Ganeti Web Manager`_. Its written using the
django framework and connecting to Ganeti via its RAPI protocol. Our lead
developer `Peter Krenesky`_ and many of our students have been hard at work on
this project in the last month and a half.

.. image:: {filename}/media/createvm.png
    :align: center
    :width: 80%
    :alt: image

Some of the goals of this project include:

-  Permission system for users and how they access the cluster(s)
-  Easy VM deployment and management
-  Console access
-  Empower VM users

We're very close to making our first release of ganeti-webmgr which should
include a basic set of features. We still have a lot to work on and I look
forward to seeing how it evolves.

.. _OSUOSL: http://osuosl.org
.. _Ganeti: http://code.google.com/p/ganeti/
.. _KVM: http://www.linux-kvm.org/page/Main_Page
.. _OSGeo: http://osgeo.org
.. _phpBB: http://www.phpbb.com
.. _ECF: http://www.eclipse.org/ecf/
.. _ganeti-instance-image: http://code.osuosl.org/projects/ganeti-image
.. _Ganeti Web Manager: http://code.osuosl.org/projects/ganeti-webmgr
.. _Peter Krenesky: http://blogs.osuosl.org/kreneskyp/
