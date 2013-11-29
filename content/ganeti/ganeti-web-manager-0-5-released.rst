Ganeti Web Manager 0.5 Released
###############################
:date: 2011-02-03 11:54
:author: lance
:tags: django, ganeti, ganeti web manager, gwm, novnc, virtualization,
  websockets
:slug: ganeti-web-manager-0-5-released

After nearly a month and a half (42 days) of development since 0.4 was released,
the `OSUOSL`_ has released `Ganeti Web Manager`_ `0.5`_ today.  This second
release has some very nice new features included in it:

-  New `status Dashboard`_
-  `Integrated`_ `noVNC`_, an HTML5 + WebSockets VNC viewer
-  New `Twisted`_ based `VNC Auth Proxy`_
-  Virtual machine `re-install`_ implemented
-  Auto-start is now an option during VM creation
-  Ram and CPU quota is now based off running virtual machines
-  Improved layout
-  Numerous bug fixes and improvements.

Read the full `ChangeLog`_ for more details.

noVNC Console
~~~~~~~~~~~~~

My favorite new feature by far is the inclusion of noVNC by default for VNC
console access. This removes the Java requirement for your browsers and makes it
much easier to use. It works the best using Chrome/Chromium but you can also use
Firefox.

.. image:: {filename}/media/novnc-console.png
    :width: 80%
    :align: center
    :alt: novnc console

New Overview Page
~~~~~~~~~~~~~~~~~

I'm also excited about the new overview pages for users and admins. It makes it
much easier to see the usage of your cluster(s) quickly. For users it will show
some basic resource/quota usage.

.. image:: {filename}/media/dashboard.png
    :align: center
    :width: 80%
    :alt: new overview page

Upgrading
~~~~~~~~~

If you're upgrading from 0.4 be sure to read the `upgrading wiki page`_ and go
over the `installation page`_ again. We've added a few new requirements such as
`South`_ for database migrations and Twisted for the new VNC Auth Proxy.

Be sure to also check out Peter's `blog post`_ about the 0.5 release as well!

.. _OSUOSL: http://osuosl.org
.. _Ganeti Web Manager: http://code.osuosl.org/projects/ganeti-webmgr
.. _0.5: http://code.osuosl.org/projects/ganeti-webmgr/files
.. _status Dashboard: http://code.osuosl.org/projects/ganeti-webmgr/wiki/Screenshots#Status-Dashboard
.. _Integrated: http://code.osuosl.org/projects/ganeti-webmgr/wiki/VNC
.. _noVNC: http://github.com/kanaka/noVNC
.. _Twisted: http://twistedmatrix.com/trac/
.. _VNC Auth Proxy: http://code.osuosl.org/projects/twisted-vncauthproxy
.. _re-install: http://code.osuosl.org/issues/765
.. _ChangeLog: http://code.osuosl.org/projects/ganeti-webmgr/wiki/CHANGELOG
.. _upgrading wiki page: http://code.osuosl.org/projects/ganeti-webmgr/wiki/Upgrading
.. _installation page: http://code.osuosl.org/projects/ganeti-webmgr/wiki/Install
.. _South: http://south.aeracode.org/
.. _blog post: http://blogs.osuosl.org/kreneskyp/2011/02/03/ganeti-web-manager-0-5/
