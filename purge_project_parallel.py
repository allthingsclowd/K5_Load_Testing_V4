#!/usr/bin/python
"""Threaded version of the purge script
This script attempts to obliterate/destroy/delete all resources in the supplied project along with fixed security groups and fixed ssh key pairs.

Don't run this as a CLOUD ADMIN as you could end up in big trouble!!!!!


Author: Graham Land
Date: 09/02/17
Twitter: @allthingsclowd
Github: https://github.com/allthingscloud
Blog: https://allthingscloud.eu


"""
from k5contractsettingsV10 import *
#from GTV10 import *
from k5APIwrappersV21 import *
# Gevent magic!
import gevent
import gevent.monkey


def purge_project(projectid, projectidB, infra):
    k5token = get_scoped_token(adminUser, adminPassword, contract, projectid, region).headers['X-Subject-Token']
    print k5token

    serverpurgelist = []

    PBK5token = get_rescoped_token(k5token, projectidB, region).headers['X-Subject-Token']
    print PBK5token

    gevent.monkey.patch_all()
    if infra:
        print "Deleting Snapshots"
        jobs = [gevent.spawn(delete_snapshot, k5token, snapshot.get('id'), projectid, region) for snapshot in list_snapshots(k5token, projectid, region).json()['snapshots']]
        result = gevent.joinall(jobs, timeout=1200)


    for server in list_servers(k5token, projectid, region).json()['servers']:
        #print server
        if server['metadata'].get('Example Custom Tag'):
            serverpurgelist.append(server.get('id'))
            print "Scheduled to delete ", server.get('name')
        else:
            print "Keeping ", server.get('name')


    print "Deleting Servers - Load Test Servers"
    jobs = [gevent.spawn(delete_server, k5token, server, projectid, region) for server in serverpurgelist]
    result = gevent.joinall(jobs, timeout=3600)


    if infra:
        for server in list_servers(k5token, projectid, region).json()['servers']:
            #print server
            if server['metadata'].get('K5 Load Test'):
                serverpurgelist.append(server.get('id'))
                print "Scheduled to delete ", server.get('name')
            else:
                print "Keeping ", server.get('name')


        print "Deleting Servers - Infrastructure Monitor Server"
        jobs = [gevent.spawn(delete_server, k5token, server, projectid, region) for server in serverpurgelist]
        result = gevent.joinall(jobs, timeout=3600)

        print "Deleting Inter AZ Network Connectors"
        for ep in list_network_connector_endpoints(k5token, region).json()['network_connector_endpoints']:
            if len(show_network_connector_ep_interfaces(k5token, ep.get('id'), region).json()['network_connector_endpoint']['interfaces']) > 0:
                for port in show_network_connector_ep_interfaces(k5token, ep.get('id'), region).json()['network_connector_endpoint']['interfaces']:
                    print disconnect_network_connector_endpoint(k5token, ep.get('id'), port.get('port_id'), region)
                    print delete_port(k5token, port.get('port_id'), region)
            print delete_network_connector_ep(k5token, ep.get('id'), region)


        for nc in list_network_connectors(k5token,region).json()['network_connectors']:
            print delete_network_connector(k5token, nc.get('id'), region)

        print "Deleting Volumes"
        jobs = [gevent.spawn(delete_volume, k5token, volume.get('id'), projectid, region) for volume in list_volumes(k5token, projectid, region).json()['volumes']]
        result = gevent.joinall(jobs, timeout=1200)

        print "Deleting Floating IPs"
        jobs = [gevent.spawn(delete_global_ip, k5token, global_ip.get('id'), region) for global_ip in list_global_ips(k5token, region).json()['floatingips']]
        result = gevent.joinall(jobs, timeout=1200)

        print "Deleting VPN Connections"
        jobs = [gevent.spawn(delete_ipsec_site_connection, k5token, vpncon.get('id'), region) for vpncon in list_ipsec_site_connections(k5token, region).json()['ipsec_site_connections']]
        result = gevent.joinall(jobs, timeout=1200)

        print "Deleting VPN Services"
        jobs = [gevent.spawn(delete_vpn_service, k5token, vpnservice.get('id'), region) for vpnservice in list_vpn_services(k5token, region).json()['vpnservices']]
        result = gevent.joinall(jobs, timeout=1200)

        print "Deleting VPN IPSec Policies"
        jobs = [gevent.spawn(delete_ipsec_policy, k5token, secpol.get('id'), region) for secpol in list_ipsec_policies(k5token, region).json()['ipsecpolicies']]
        result = gevent.joinall(jobs, timeout=1200)

        for router in list_routers(k5token, region).json()['routers']:
            if len(router['routes']) > 0:
                print update_router_routes(k5token, router.get('id'), None, region)

            print "Deleting Router Interfaces"
            jobs = [gevent.spawn(remove_interface_from_router, k5token, router.get('id'), interface.get('id'), region) for interface in show_router_interfaces(k5token, router.get('id'), region).json()['ports']]
            result = gevent.joinall(jobs, timeout=1200)

            print "Deleting InterProject Ports"
            jobs = [gevent.spawn(inter_project_connection_remove, k5token, port.get('device_id'), port.get('id'), region) for port in list_ports(PBK5token, region).json()['ports']]
            result = gevent.joinall(jobs, timeout=1200)

            print "Deleting InterProject Ports - take2 "
            jobs = [gevent.spawn(inter_project_connection_remove, PBK5token, port.get('device_id'), port.get('id'), region) for port in list_ports(PBK5token, region).json()['ports']]
            result = gevent.joinall(jobs, timeout=1200)

        print "Deleting Routers"
        jobs = [gevent.spawn(delete_router, k5token, router.get('id'), region) for router in list_routers(k5token, region).json()['routers']]
        result = gevent.joinall(jobs, timeout=1200)

        print "Deleting Ports"
        jobs = [gevent.spawn(delete_port, k5token, port.get('id'), region) for port in list_ports(k5token, region).json()['ports']]
        result = gevent.joinall(jobs, timeout=1200)

        print "Only purging very specific security groups - modify this to Purge ALL SGs"
        for sg in list_security_groups(k5token, region).json()['security_groups']:
            #if "created by API" in sg.get('description'):
            if "Demo Security Group Allows RDP, SSH and ICMP" in sg.get('description'):
                result = delete_security_group(k5token, sg.get('id'), region)
                if result.status_code == 204:
                    print "Security group removed - ", sg.get('id')
                else:
                    print "Security group delete error: ", result.json()

        print "Only purging very specific key pairs - modify this to Purge ALL key pairs"
        for kp in list_keypairs(k5token, projectid, region).json()['keypairs']:

            if "k5-loadtest" in kp['keypair'].get('name'):
                result = delete_keypair(k5token, kp['keypair'].get('name'), projectid, region)
                print result
                if result.status_code == 202:
                    print "SSH KP removed - ", kp['keypair'].get('name')
                else:
                    print "SSH KP delete error: ", result.json()

        print "Deleting Subnets"
        jobs = [gevent.spawn(delete_subnet, k5token, subnet.get('id'), region) for subnet in list_subnets(k5token, region).json()['subnets']]
        result = gevent.joinall(jobs, timeout=1200)

        print "Deleting Networks"
        jobs = [gevent.spawn(delete_network, k5token, network.get('id'), region) for network in list_networks(k5token, region).json()['networks']]
        result = gevent.joinall(jobs, timeout=1200)


def main():


    purge_project(demoProjectAid, demoProjectAid, buildInfrastructure)


if __name__ == "__main__":
    main()
