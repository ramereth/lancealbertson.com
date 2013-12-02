Ganeti Web Manager 0.4 released
###############################
:date: 2010-12-22 14:40
:author: lance
:tags: django, ganeti, ganeti web interface, ganeti-webmgr, virtualization,
  planet
:slug: ganeti-web-manager-0-4-released

.. image:: {filename}/media/gwm-logo.png
   :align: right
   :alt: Ganeti Web Manager logo

After three months of development `Ganeti Web Manager`_ 0.4 has been released!
This project has been developed primarily by the `OSU Open Source Lab`_ with
help from the folks at `GRNET`_ and several `Google GCI`_ students. Ganeti Web
Manager (GWM) is a Django-based web application that connects to the `Ganeti
Remote API`_. It allows Ganeti administrators access to the various common
tasks along with incorporating a permission system. GWM has a long ways to go
in terms of implementing more of the RAPI features and UI improvements but this
first release should be enough to get people to start using it in production.
You can download Ganeti Web Manager `here`_.

Features in 0.4:
----------------

-  `Caching system`_
-  `Permissions system`_:
   -  User & Group management
   -  Per cluster/virtual machine permissions
-  Basic VM management: Create, Delete, Start, Stop, Reboot, VNC Console
-  `SSH key feed`_ (for a ganeti post-install hook)
-  Basic quota system
-  Import tools

Basic Installation Requirements
-------------------------------

GWM has a fairly low requirement footprint and only requires a minimum amount
of Django dependencies.

-  `Django`_ >= 1.2
-  `django-registration`_
-  `object\_permissions`_ (packaged with releases)
-  sqlite3, mysql, or postgresql

Currently Firefox and Chrome browsers should work well although know that IE
will have issues. I certainly hope whoever is using this application has at
least Firefox installed. You will need the Java browser plugin in order to the
VNC console. The VNC console requires direct access to the VNC port on the VM
but we are working with GRNET to add in a `VNC Auth Proxy`_ to get around that.

Ganeti compatibility:
---------------------

-  >= 2.2.x - supported
-  2.1.x - mostly supported
-  2.0.x - unsupported but may work
-  1.x - unsupported

Screenshots:
------------

List all virtual machines on a cluster:

.. image:: {filename}/media/cluster-vm-tab.png
    :align: center
    :width: 80%
    :alt: List VMs in a cluster

Creating a new virtual machine form:

.. image:: {filename}/media/vm-add.png
    :align: center
    :width: 80%
    :alt: Creating a new virtual machine

Virtual machine reation output dynamically updating:

.. image:: {filename}/media/vm-create-output.png
    :align: center
    :width: 80%
    :alt: VM Creation output

Virtual machine VNC console using the java client.

.. image:: {filename}/media/vm-console.png
    :align: center
    :width: 80%
    :alt: VM VNC Console

Upcoming Features
-----------------

We have lots of features we would like to eventually implement in GWM.  You can
see many of them on our `issue tracker`_ but here's a summary of notable
features we plan to do.

-  VM Management: `Modify`_, `Reinstall`_, Migrate/Failover
-  Improve usability of forms
-  `Optional NoVNC console access`_
-  `Serial console support`_
-  Implement the rest of the RAPI features that are supported
-  `VM Creation templates`_
-  VNC Proxy

I'm excited to see where Ganeti Web Manager goes. I plan to start rolling it
out at the OSUOSL very soon and giving access to some of the projects we host.
If you would like to become a contributor to the project, please check us out
on IRC in #ganeti-webmgr on Freenode.

Check my blog and `Peter's blog`_ for more updates soon on Ganeti Web Manager.

.. _Ganeti Web Manager: http://code.osuosl.org/projects/ganeti-webmgr
.. _OSU Open Source Lab: http://osuosl.org
.. _GRNET: http://www.grnet.gr/
.. _Google GCI: http://code.google.com/opensource/gci/2010-11/index.html
.. _Ganeti Remote API: http://docs.ganeti.org/ganeti/current/html/rapi.html
.. _here: https://code.osuosl.org/projects/ganeti-webmgr/files
.. _Caching system: http://code.osuosl.org/projects/ganeti-webmgr/wiki/Cache_System
.. _Permissions system: http://code.osuosl.org/projects/ganeti-webmgr/wiki/Permissions
.. _SSH key feed: http://code.osuosl.org/projects/ganeti-webmgr/wiki/PermissionsSSHKeys
.. _Django: http://www.djangoproject.com/
.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/
.. _object\_permissions: http://code.osuosl.org/projects/object-permissions
.. _VNC Auth Proxy: https://code.grnet.gr/projects/vncauthproxy
.. _issue tracker: http://code.osuosl.org/projects/ganeti-webmgr/issues
.. _Modify: http://code.osuosl.org/issues/693
.. _Reinstall: http://code.osuosl.org/issues/765
.. _Optional NoVNC console access: http://code.osuosl.org/issues/1935
.. _Serial console support: http://code.osuosl.org/issues/2217
.. _VM Creation templates: http://code.osuosl.org/issues/759
.. _Peter's blog: http://blogs.osuosl.org/kreneskyp/
