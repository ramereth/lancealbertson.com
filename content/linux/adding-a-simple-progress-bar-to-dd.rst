Adding a simple progress bar to dd
##################################
:date: 2009-04-27 21:35
:author: lance
:tags: bar, dd, kvm, lvm, migration
:slug: adding-a-simple-progress-bar-to-dd

I recently ran into an issue where I wanted to move several `KVM`_ based virtual
machines from one server to another server. There's several ways you can
accomplish this depending on what you want to do. In my case I was using `LVM`_
for the disk backend, so simply copying the disk image files wasn't an option.
It boiled down to two basic options.

-  Put system in single-user mode, rsync the contents over, and
   reinstall grub
-  Use dd and copy the whole LVM volume over piped through ssh

The advantage using the rsync method is that you're only copying the files you
need over, thus less data transfer happens. But then you run into needing to
re-run grub (which generally isn't a problem). In addition, if you're using LVM
within the LVM volume for the VM and the volume group is named the same, you run
into some interesting issues.  The advantage for using **dd** is that you can
get a literal copy of the disk image and just start the VM back up without any
other steps. Of course, this will only work if the volumes are the same on both
ends.

So I decided to go with dd but ran into a problem of seeing the progress of a
15G volume copy. I did some digging around and found a `blog post`_ that
mentioned using a command line application called '`bar`_' so I decided to give
it a shot! Its a fairly simple application that just creates a basic progress
bar based on the data being piped into it. If you're running Gentoo, the package
is called **app-admin/bar**.

Here's the command I ended up running::

    $ dd if=/dev/lvm/cholula-disk | bar -s 15g | \
      ssh -c arcfour $host "dd of=/dev/lvm/cholula-disk"

When ran, it gives you output similar to::

    6.0GB at 17.9MB/s eta: 0:08:32 40 [========================= ]

The downside is that you need to specify the block device size before hand, but
for something simple like this its quite nice. Of course I could just use one of
the many dd forks out there which include progress bars but this is quick,
dirty, and simple!

I used the arcfour cipher mainly to reduce the CPU overhead and increase the
throughput, but you should probably never use this cipher on an untrusted
network as it does have weaknesses. I didn't try doing throughput tests on other
ciphers, but it would be interesting. It took me approximately 10-12 minutes to
copy a 15G volume over a gigabit network which isn't too bad.

Another trick you can do is utilitize the LVM snapshot feature and create a
snapshot of the running volume. If any data changes on the volume, it won't be
copied over obviously, but it will at least let you do a cold "live" migration
of sorts.

.. _KVM: http://www.linux-kvm.org/page/Main_Page
.. _LVM: http://en.wikipedia.org/wiki/Logical_Volume_Manager_(Linux)
.. _blog post: http://fosswire.com/post/2007/8/command-line-progress-bar-a-progress-bar-for-dd/
.. _bar: http://clpbar.sourceforge.net/
