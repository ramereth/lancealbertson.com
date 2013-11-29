Managing Ganeti with finer control
##################################
:date: 2010-12-28 18:06
:author: lance
:tags: django, ganeti, ganeti web interface, ganeti-webmgr, virtualization
:slug: managing-ganeti-with-finer-control

Lead `OSUOSL`_ Developer `Peter Krenesky`_ has written an excellent `blog post`_
going over how the permission system works in `Ganeti Web Manager`_. A key
feature I'm looking forward to using more at the OSUOSL is managing our clusters
with the following scenarios:

-  **Fully managed -** users have no access at all. Only admins can create,
   reboot, or modify.
-  **Partially managed -** users can’t create virtual machines, but they have
   some limited ability to manage them.
-  **Self Service -** users can create virtual machines on demand. They can
   create and manage their own virtual machines as needed.
-  **User Managed Cluster -** a user has control of an entire cluster.

The permission system in GWM will enable Ganeti cluster admins the ability to
manage each cluster and virtual machine in finer detail.  `Ganeti`_ by itself
doesn't come with any sort of user access management system, nor should it
really. It makes sense to build tools like GWM on top of Ganeti to deal with
such situations. I hope to see more features and bug fixes related to the
permissions and quota system.

I'd love to see some feedback on how we implemented the system and how we can
improve it!

.. _OSUOSL: http://osuosl.org
.. _Peter Krenesky: http://blogs.osuosl.org/kreneskyp
.. _blog post: http://blogs.osuosl.org/kreneskyp/2010/12/28/ganeti-web-manager-permissions/
.. _Ganeti Web Manager: http://code.osuosl.org/projects/ganeti-webmgr
.. _Ganeti: http://code.google.com/p/ganeti/
