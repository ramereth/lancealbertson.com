Handling HDD failures with Ganeti
#################################
:date: 2011-02-05 12:40
:author: lance
:tags: drbd, evacuate, failover, ganeti, gnt-instance, gnt-node, hard drive
  failure, outage, replace-disks, virtualization, planet
:slug: handling-hdd-failures-with-ganeti

Recently I had one of the nodes in a `Ganeti`_ cluster go down because of a
faulty hard drive. Normally we would have RAID on machines in our ganeti
clusters, but this particular machine didn't. Having a machine go offline like
that would usually be a big deal, but with ganeti and `DRBD`_ this isn't the
case usually.

After I triaged the situation and decided that the HDD on the machine node3 was
a lost cause, I decided to see what ganeti showed as the situation. Below is
what I found::

    $ gnt-cluster verify
    * Verifying global settings
    * Gathering data (3 nodes)
    * Verifying node status
      - ERROR: node node1.osuosl.bak: ssh communication with node 'node3.osuosl.bak': ssh problem: exited with exit code 255 (no output)
      - ERROR: node node1.osuosl.bak: tcp communication with node 'node3.osuosl.bak': failure using the primary and secondary interface(s)
      - ERROR: node node2.osuosl.bak: ssh communication with node 'node3.osuosl.bak': ssh problem: exited with exit code 255 (no output)
      - ERROR: node node2.osuosl.bak: tcp communication with node 'node3.osuosl.bak': failure using the primary and secondary interface(s)
      - ERROR: node node3.osuosl.bak: while contacting node: Error 7: Failed connect to 10.1.0.179:1811; Success
    * Verifying instance status
      - ERROR: node node3.osuosl.bak: instance vm1.osuosl.org, connection to secondary node failed
      - ERROR: node node3.osuosl.bak: instance vm2.osuosl.org, connection to secondary node failed
      - ERROR: node node3.osuosl.bak: instance vm3.osuosl.org, connection to secondary node failed
      - ERROR: instance vm4.osuosl.org: instance not running on its primary node node3.osuosl.bak
      - ERROR: node node3.osuosl.bak: instance vm4.osuosl.org, connection to primary node failed
      - ERROR: instance vm5.osuosl.org: instance not running on its primary node node3.osuosl.bak
      - ERROR: node node3.osuosl.bak: instance vm5.osuosl.org, connection to primary node failed
    * Verifying orphan volumes
    * Verifying orphan instances
    * Verifying N+1 Memory redundancy
      - ERROR: node node3.osuosl.bak: not enough memory on to accommodate failovers should peer node node1.osuosl.bak fail
      - ERROR: node node3.osuosl.bak: not enough memory on to accommodate failovers should peer node node2.osuosl.bak fail
    * Other Notes
      - WARNING: Communication failure to node node3.osuosl.bak: Error 7: Failed connect to 10.1.0.179:1811; Success
    * Hooks Results
      - ERROR: node node3.osuosl.bak: Communication failure in hooks execution: Error 7: Failed connect to 10.1.0.179:1811; Success

That's a lot of information to just say one of the nodes is offline. To
summarize, this is what Ganeti is saying:

-  node1 & node2 can't talk to node3
-  node3 isn't responding to the master node
-  vm1, vm2, vm3's secondary drbd connection failed
-  vm4 & vm5 is not running
-  node3 doesn't have enough memory to deal with failovers (probably because
   ganeti can't see its resources)
-  node3 connections failure

Needless to say, node3 is down. Now lets mark node3 offline and see what ganeti
shows::

    $ gnt-node modify -O yes node3
      - WARNING: Communication failure to node node3.osuosl.bak: Error 7: Failed connect to 10.1.0.179:1811; Success
    $ gnt-cluster verify
    * Verifying node status
    * Verifying instance status
      - ERROR: instance vm1.osuosl.org: instance lives on offline node(s) node3.osuosl.bak
      - ERROR: instance vm2.osuosl.org: instance lives on offline node(s) node3.osuosl.bak
      - ERROR: instance vm3.osuosl.org: instance lives on offline node(s) node3.osuosl.bak
      - ERROR: instance vm4.osuosl.org: instance lives on offline node(s) node3.osuosl.bak
      - ERROR: instance vm5.osuosl.org: instance lives on offline node(s) node3.osuosl.bak
    * Verifying orphan volumes
    * Verifying orphan instances
    * Verifying N+1 Memory redundancy
      - ERROR: node node3.osuosl.bak: not enough memory on to accommodate failovers should peer node node1.osuosl.bak fail
      - ERROR: node node3.osuosl.bak: not enough memory on to accommodate failovers should peer node osdv2.osuosl.bak fail
    * Other Notes
      - NOTICE: 1 offline node(s) found.
    * Hooks Results

That's much easier to read and handle. At this point I'm ready to failover the
instances that are offline::

    $ gnt-instance failover --ignore-consistency vm4
    * checking disk consistency between source and target
    * shutting down instance on source node
      - WARNING: Could not shutdown instance vm4.osuosl.org on node node3.osuosl.bak. Proceeding anyway. Please make sure node node3.osuosl.bak is down. Error details: Node is marked offline
    * deactivating the instance's disks on source node
      - WARNING: Could not shutdown block device disk/0 on node node3.osuosl.bak: Node is marked offline
    * activating the instance's disks on target node
      - WARNING: Could not prepare block device disk/0 on node node3.osuosl.bak (is_primary=False, pass=1): Node is marked offline
    * starting the instance on the target node
    $ gnt-instance failover --ignore-consistency vm5

Now lets fix the secondary storage for the other instances::

    $ gnt-instance replace-disks -n node2 vm1
     - INFO: Old secondary node3.osuosl.bak is offline, automatically
    enabling early-release mode
    Replacing disk(s) 0 for vm1.osuosl.org
    STEP 1/6 Check device existence
     - INFO: Checking disk/0 on node1.osuosl.bak
     - INFO: Checking volume groups
    STEP 2/6 Check peer consistency
     - INFO: Checking disk/0 consistency on node node1.osuosl.bak
    STEP 3/6 Allocate new storage
     - INFO: Adding new local storage on node2.osuosl.bak for disk/0
    STEP 4/6 Changing drbd configuration
     - INFO: activating a new drbd on node2.osuosl.bak for disk/0
     - INFO: Shutting down drbd for disk/0 on old node
     - WARNING: Failed to shutdown drbd for disk/0 on oldnode: Node is marked offline
          Hint: Please cleanup this device manually as soon as possible
     - INFO: Detaching primary drbds from the network (=> standalone)
     - INFO: Updating instance configuration
     - INFO: Attaching primary drbds to new secondary (standalone => connected)
    STEP 5/6 Removing old storage
     - INFO: Remove logical volumes for 0
     - WARNING: Can't remove old LV: Node is marked offline
          Hint: remove unused LVs manually
     - WARNING: Can't remove old LV: Node is marked offline
          Hint: remove unused LVs manually
    STEP 6/6 Sync devices
     - INFO: Waiting for instance vm1.osuosl.org to sync disks.
     - INFO: - device disk/0: 0.00% done, no time estimate
     - INFO: - device disk/0: 25.00% done, 2h 23m 24s remaining (estimated)
     - INFO: - device disk/0: 50.40% done, 47m 38s remaining (estimated)
     - INFO: - device disk/0: 76.40% done, 26m 46s remaining (estimated)
     - INFO: - device disk/0: 92.20% done, 7m 49s remaining (estimated)
     - INFO: - device disk/0: 100.00% done, 0s remaining (estimated)
     - INFO: Instance vm1.osuosl.org's disks are in sync.

By using ``--submit`` you are able to let the output go into the background. You
can view the output in real-time by running ``gnt-job watch <job id>``. I went
ahead and told ganeti replace the secondary disks on the other two machines at
the same time. Be careful running too many replace disk operations as you may
run into disk I/O issues on the nodes.

Now there is another way I could have fixed this and would have required less
steps by using ``gnt-node evacuate``. This command allows you to move all the
secondary storage from a single node to another node quickly instead of doing it
vm-by-vm. The command probably would have looked something similar to this::

  $ gnt-node evacuate --force -n node2 node3

Instead of specifying which node to migrate storage to, you can also use an
IAllocator plugin to automatically pick which node to use. So the command above
would have been::

  $ gnt-node evacuate --force -I hail node3

After a few minutes I brought redundancy back into my cluster, instances back
online, an with no data loss.

Ganeti rocks!

.. _Ganeti: http://code.google.com/p/ganeti/
.. _DRBD: http://www.drbd.org
