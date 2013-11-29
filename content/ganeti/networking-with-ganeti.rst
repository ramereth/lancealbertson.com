Networking with Ganeti
######################
:date: 2011-03-12 18:07
:author: lance
:tags: bridge interface, ganeti, gentoo, network setup, virtualization, vlan
:slug: networking-with-ganeti

I've been asked quite a bit about how I do our network setup with Ganeti. I
admit that it did take me a bit to figure out a sane way to do it in Gentoo.
Unfortunately (at least in baselayout-1.x) bringing up VLANs with bridge
interfaces in Gentoo is rather a pain. What I'm about to describe is basically a
hack and there's probably a better way to do this. I hope it gets improved in
baselayout-2.x but I haven't had a chance to take a look. Please feel free to
add comments on what you feel will work better.

The key problem I ran into was dealing with starting up the vlan interfaces
first, then starting up the bridged interfaces in the correct order. Here's a
peek at the network config on one of our Ganeti hosts on Gentoo:

.. code-block:: bash

    # bring up bridge interfaces manually after eth0 is up
    postup() {
      local vlans="42 113"
      if [ "${IFACE}" = "eth0" ] ; then
        for vlan in $vlans ; do
          /etc/init.d/net.br${vlan} start
          if [ "${vlan}" = "113" ] ; then
            # make sure the bridges get going first
            sleep 10
          fi
        done
      fi
    }

    # bring down bridge interfaces first
    predown() {
      local vlans="42 113"
      if [ "${IFACE}" = "eth0" ] ; then
        for vlan in $vlans ; do
          /etc/init.d/net.br${vlan} stop
        done
      fi
    }

    # Setup trunked VLANs
    vlans_eth0="42 113"
    config_eth0=( "null" )
    vconfig_eth0=( "set_name_type VLAN_PLUS_VID_NO_PAD" )
    config_vlan42=( "null" )
    config_vlan113=( "null" )

    # Bring up primary IP on eth0 via the bridged interface
    bridge_br42="vlan42"
    config_br42=( "10.18.0.150 netmask 255.255.254.0" )
    routes_br42=( "default gw 10.18.0.1" )

    # Setup bridged VLAN interfaces
    bridge_br113="vlan113"
    config_br113=( "null" )

    # Backend drbd network
    config_eth1=( "192.168.19.136 netmask 255.255.255.0" )

The latter portion of the config its fairly normal. I setup eth0 to null, set
the VLAN's to null, then I add settings to the bridge interfaces. In our case
we have the IP for the node itself on br42. The rest of the VLAN's are just set
to null. Finally we setup the backend secondary IP.

The first part of the config is the "fun stuff". In order for this to work you
need to only add net.eth0 and net.eth1 to the default enabled level. The
post\_up() function will start the bridge interfaces after eth0 has started and
iterates through the list of vlans/bridges. Since I'm using the bridge
interface as the primary host connection, I added a simple sleep at the end to
let it see the traffic first.

That's it! A fun hack that seems to work. I would love to hear feedback on this
:)
