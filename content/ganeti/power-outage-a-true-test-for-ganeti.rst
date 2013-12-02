Power Outage: A true test for Ganeti
####################################
:date: 2010-05-20 17:06
:author: lance
:tags: drbd, ganeti, kvm, power outage, virtualization, planet
:slug: power-outage-a-true-test-for-ganeti

Nothing like a power outage gone wrong to test a new virtualization cluster.
Last night we lost power in most of Corvallis and our UPS & Generator functioned
properly in the machine room. However we had an unfortunate sequence of issues
that caused some of our machines to go down, including all **four** of our
ganeti nodes hosting **62 virtual machines** went down hard. If this had
happened with our old xen cluster with iSCSI, it would have taken us over an
hour to get the infrastructure back in a normal state by manually restarting
each VM.

But when I checked the `ganeti`_ cluster shortly after the outage, I noticed
that all four nodes rebooted without any issues and the master node was
**already** rebooting virtual machines **automatically** and fixing all of the
`DRBD`_ block devices. Ganeti has a nice app called ``ganeti-watcher`` which
is run every five minutes via cron. It has two primary functions currently
(taken from ``ganeti-watcher(8))``:

#. Keep running all instances as marked (i.e. if they were running, restart
   them)
#. Repair DRBD links by reactivating the block devices of instances which have
   secondaries on nodes that have rebooted.

The watcher app took around 30 minutes to bring all 62 VMs back online.  The
load on most of the nodes didn't go over 4 during the recovery which is quite
impressive considering how much I/O its doing while VMs are booting. Normally
the nodes have loads between 0.3 and 0.5. There were only 3 VMs that didn't boot
cleanly because of incorrect fstab entries or incorrect kernel path settings in
ganeti which was easy to fix. I was surprised we didn't have more issues like
that.

While ganeti is bringing instances back online you can tail watcher.log which is
generally at ``/var/log/ganeti/watcher.log`` and will show output similar to
this::

    2010-05-20 04:06:25,077: pid=10202 INFO Restarting busybox.osuosl.org (Attempt #1)
    2010-05-20 04:07:16,311: pid=10202 INFO Restarting driverdev.osuosl.org (Attempt #1)
    2010-05-20 04:07:18,346: pid=10202 INFO Restarting pcc.osuosl.org (Attempt #1)

And once its finished will show output like this::

    2010-05-20 04:35:04,066: pid=22741 INFO Restart of busybox.osuosl.org succeeded
    2010-05-20 04:35:04,066: pid=22741 INFO Restart of driverdev.osuosl.org succeeded
    2010-05-20 04:35:04,066: pid=22741 INFO Restart of pcc.osuosl.org succeeded

It was great watching this system recover everything automatically with little
issues and quickly. Needless to say, outages are a bad thing and its our fault
that our cluster went down like this but it was great seeing this system work
nearly flawlessly. We'll soon fix the power situation for our cluster so this
shouldn't happen again.

Take that ESX ;-)

.. _ganeti: http://code.google.com/p/ganeti/
.. _DRBD: http://www.drbd.org/
