Rebalancing Ganeti Clusters
###########################
:date: 2011-05-02 22:55
:author: lance
:tags: ganeti, hbal, htools, iaas, private cloud, rebalancing ganeti, virtualization
:slug: rebalancing-ganeti-clusters

One of the best features of Ganeti is its ability to grow *linearly* by adding
new servers easily. We recently purchased a new server to expand our ever
growing production cluster and needed to rebalance cluster.  Adding and
expanding the cluster consisted of the following steps:

#. Installing the base OS on the new node
#. Adding the node to your configuration management of choice and/or installing
   ganeti
#. Add the node to the cluster with **gnt-node add**
#. Check Ganeti using the verification action
#. Use htools to rebalance the cluster

For simplicity sake I'll cover the last three steps.

Adding the node
~~~~~~~~~~~~~~~

Assuming you're using a secondary network, this is how you would add
your node::

    gnt-node add -s <secondary ip> newnode

Now lets check and make sure ganeti is happy::

    gnt-cluster verify

If all is well, continue on otherwise try and resolve any issue that ganeti is
complaining about.

Using htools
~~~~~~~~~~~~

Make sure you install ganeti-htools on all your nodes before continuing.  It
requires haskell so just be aware of that requirement. Lets see what htools
wants to do first::

    $ hbal -m ganeti.example.org
    Loaded 5 nodes, 73 instances
    Group size 5 nodes, 73 instances
    Selected node group: default
    Initial check done: 0 bad nodes, 0 bad instances.
    Initial score: 41.00076094
    Trying to minimize the CV...
    1. openmrs.osuosl.org g1.osuosl.bak:g2.osuosl.bak g5.osuosl.bak:g1.osuosl.bak 38.85990831 a=r:g5.osuosl.bak f
    2. stagingvm.drupal.org g3.osuosl.bak:g1.osuosl.bak g5.osuosl.bak:g3.osuosl.bak 36.69303985 a=r:g5.osuosl.bak f
    3. scratchvm.drupal.org g2.osuosl.bak:g4.osuosl.bak g5.osuosl.bak:g2.osuosl.bak 34.61266967 a=r:g5.osuosl.bak f

    <snip>

    28. crisiscommons1.osuosl.org g3.osuosl.bak:g1.osuosl.bak g3.osuosl.bak:g5.osuosl.bak 4.93089388 a=r:g5.osuosl.bak
    29. crisiscommons-web.osuosl.org g2.osuosl.bak:g1.osuosl.bak g1.osuosl.bak:g5.osuosl.bak 4.57788814 a=f r:g5.osuosl.bak
    30. aqsis2.osuosl.org g1.osuosl.bak:g3.osuosl.bak g1.osuosl.bak:g5.osuosl.bak 4.57312216 a=r:g5.osuosl.bak
    Cluster score improved from 41.00076094 to 4.57312216
    Solution length=30

I've shortened the actual output for the sake of this blog post. Htools
automatically calculates which virtual machines to move and how using the least
amount of operations. In most these moves, the VMs may simply be migrated,
migrated & secondary storage replaced, or migrated, secondary storage replaced,
migrated. In our environment we needed to move 30 VMs around out of the total
70 VMs that are hosted on the cluster.

Now lets see what commands we actually would need to run::

    $ hbal -C -m ganeti.example.org

    Commands to run to reach the above solution:

    echo jobset 1, 1 jobs
    echo job 1/1
    gnt-instance replace-disks -n g5.osuosl.bak openmrs.osuosl.org
    gnt-instance migrate -f openmrs.osuosl.org
    echo jobset 2, 1 jobs
    echo job 2/1
    gnt-instance replace-disks -n g5.osuosl.bak stagingvm.drupal.org
    gnt-instance migrate -f stagingvm.drupal.org
    echo jobset 3, 1 jobs
    echo job 3/1
    gnt-instance replace-disks -n g5.osuosl.bak scratchvm.drupal.org
    gnt-instance migrate -f scratchvm.drupal.org

    <snip\>

    echo jobset 28, 1 jobs
    echo job 28/1
    gnt-instance replace-disks -n g5.osuosl.bak crisiscommons1.osuosl.org
    echo jobset 29, 1 jobs
    echo job 29/1
    gnt-instance migrate -f crisiscommons-web.osuosl.org
    gnt-instance replace-disks -n g5.osuosl.bak crisiscommons-web.osuosl.org
    echo jobset 30, 1 jobs
    echo job 30/1
    gnt-instance replace-disks -n g5.osuosl.bak aqsis2.osuosl.org

Here you can see the commands it wants you to execute. Now you can either put
these all in a script and run them, split them up, or just run them one by one.
In our case I ran them one by one just to be sure we didn't run into any
issues. I had a couple of VMs not migration properly but those were exactly
fixed. I split this up into a three day migration running ten jobs a day.

The length of time that it takes to move each VM depends on the following
factors:

#. How fast your secondary network is
#. How busy the nodes are
#. How fast your disks are

Most of our VMs ranged in size from 10G to 40G in size and on average took
around 10-15 minutes to complete each move. Addtionally, make sure you read the
man page for **hbal** to see all the various features and options you can
tweak. For example, you could tell **hbal** to just run all the commands for
you which might be handy for automated rebalancing.

Conclusion
~~~~~~~~~~

Overall the rebalancing of our cluster went without a hitch outside of a few
minor issues. Ganeti made it really easy to expand our cluster with minimal to
zero downtime for our hosted projects.
