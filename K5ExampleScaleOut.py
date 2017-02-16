#!/usr/bin/python
"""The following script demonstrates how to deploy up to large volumes of virtual machines balanced evenly across  a  region.


Author: Graham Land
Date: 09/02/17
Twitter: @allthingsclowd
Github: https://github.com/allthingscloud
Blog: https://allthingscloud.eu


"""

import requests
import sys
import json
import pprint
import datetime
import time
import random
import string
import copy
from multiprocessing import Process, Queue
from k5contractsettingsV10 import *


def randomword(length):
    """Generate a random string
    Args:
        length (int): length of random string required

    Returns:
        TYPE: random string of length supplied
    """
    return ''.join(random.choice(string.lowercase) for i in range(length))


def create_network_connector(k5token, projectid, connector_name):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contract (TYPE): Description
        projectid (TYPE): Description
        connector_name (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connectors')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                 headers={
                                     'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={"network_connector":
                                       {"name": connector_name,
                                        "tenant_id": projectid}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def create_network_connector_endpoint(k5token, projectid, ep_name, nc_id, az_name):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contract (TYPE): Description
        projectid (TYPE): Description
        ep_name (TYPE): Description
        nc_id (TYPE): Description
        az_name (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connector_endpoints')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                 headers={
                                     'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={"network_connector_endpoint": {
                                     "name": ep_name,
                                       "network_connector_id": nc_id,
                                       "endpoint_type": "availability_zone",
                                       "location": az_name,
                                       "tenant_id": projectid
                                       }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def connect_network_connector_endpoint(k5token, ep_id, port_id):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contract (TYPE): Description
        projectid (TYPE): Description
        ep_id (TYPE): Description
        port_id (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connector_endpoints/') + \
                                unicode(ep_id) + unicode('/connect')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.put(networkURL,
                                headers={
                                    'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={"interface":
                                      {"port_id": port_id
                                       }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def disconnect_network_connector_endpoint(k5token, ep_id, port_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contract (TYPE): Description
        projectid (TYPE): Description
        ep_id (TYPE): Description
        port_id (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connector_endpoints/') + \
                                unicode(ep_id) + unicode('/disconnect')
    print networkURL
    try:
        response = requests.put(networkURL,
                                headers={
                                    'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={"interface":
                                      {"port_id": port_id
                                       }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def list_network_connectors(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contractid (TYPE): Description
        projectid (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connectors')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.get(networkURL,
                                headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def list_network_connector_endpoints(k5token, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        contractid (TYPE): Description
        projectid (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connector_endpoints')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.get(networkURL,
                                headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def show_network_connector_ep_interfaces(k5token, endpoint_id):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        projectid (TYPE): Description
        endpoint_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connector_endpoints/') +\
                                unicode(endpoint_id) + unicode('/interfaces')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.get(networkURL,
                                headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_network_connector_details(k5token, connector_id):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        projectid (TYPE): Description
        connector_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connectors/') +\
                                unicode(connector_id)
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.get(networkURL ,
                                headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def show_network_connector_ep_details(k5token, endpoint_id):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        projectid (TYPE): Description
        endpoint_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connector_endpoints/') +\
                                unicode(endpoint_id)
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.get(networkURL,
                                headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def delete_network_connector_ep(k5token, endpoint_id, region):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        projectid (TYPE): Description
        endpoint_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connector_endpoints/') +\
                                unicode(endpoint_id)
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.delete(networkURL,
                                   headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())



def delete_network_connector(k5token, connector_id):
    """Summary

    Args:
        adminUser (TYPE): Description
        adminPassword (TYPE): Description
        projectid (TYPE): Description
        connector_id (TYPE): Description
        contract (TYPE): Description
        region (TYPE): Description

    Returns:    # serverips = []
    # print serverips
    # k5token = get_scoped_token(adminUser, adminPassword, contract, demoProjectAid, region).headers['X-Subject-Token']
    # for server in list_servers(k5token, demoProjectAid, region).json()['servers']:
    #     for nic in server.get('addresses'):
    #         if server.get('addresses')[nic][0].get('addr') not in serverips:
    #             serverips.append(server.get('addresses')[nic][0].get('addr'))
    #             print server.get('addresses')[nic][0].get('addr')
    # print serverips
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/network_connectors/') + unicode(connector_id)
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.delete(networkURL,
                                   headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def create_ep_port_pairs(k5token, projectid, newConnector, networkList, security_group_id, az):
    ncPortidList = []
    ncPortipList = []
    newConnectorid = newConnector.json()['network_connector'].get('id')
    newConnectorname = newConnector.json()['network_connector'].get('name')

    # create endpoint connector
    epname = unicode('ncep-') + unicode(az) + unicode(newConnectorname)
    Endpoint = create_network_connector_endpoint(k5token, projectid, epname, newConnectorid, az)
    print "New Endpoint --> ", Endpoint.json()

    Endpointid = Endpoint.json()['network_connector_endpoint'].get('id')

    # create the ports to add to network connector
    print "\nNetwork List \n", networkList
    for network in networkList:
        # create the ports
        Portname = unicode('ncport-') + unicode(newConnectorname) + unicode(randomword(5))
        ncPort = create_port(k5token, Portname, network[0], security_group_id, az)
        ncPortid = ncPort.json()['port'].get('id')
        ncPortip = ncPort.json()['port']['fixed_ips'][0].get('ip_address')
        ncPortidList.append(ncPortid)
        ncPortipList.append(ncPortip)
        nc = connect_network_connector_endpoint(k5token, Endpointid, ncPortid)
        print "Results of Adding Port to Endpoint >>>>>>>>>>>> ", nc
        print nc.json()

    return ("Network Connector Endpoint & Ports Created", ncPortidList, ncPortipList)


def create_inter_az_link(k5token, projectid, netidaz1, netidaz2, az1, az2,  security_group_id):

    # create the inter az connector
    newConnectorname = unicode('InterAZlink-') + unicode(randomword(5))
    newConnector = create_network_connector(k5token, projectid, newConnectorname)

    # add all az1 interfaces to network connector
    az1Connections = create_ep_port_pairs(k5token, projectid, newConnector, netidaz1, security_group_id, az1)
    # add all az2 interfaces to network connector
    az2Connections = create_ep_port_pairs(k5token, projectid, newConnector, netidaz2, security_group_id, az2)

    return (az1Connections, az2Connections)





def verify_servers_active(queue, k5token, testResults, errorOffset):
    """
    Monitor the progress of the server builds from the control plane
    Log the results when changes are detected
    Runs in it's own queue

    Args:
        k5token (object): valid project scoped k5 token
        testResults (list): list to hold the current test results
        errorOffset (int): existing errors to be ignored in project

    Returns:
        TYPE: a list containing the test results
    """
    # initialise vars
    serverips = []
    server = {"activecount": None, "timestamp": None, "errorcount": None, "average": None}
    currentts = str(datetime.datetime.utcnow())
    serverBuildTotal = testResults['servercount']
    current_server_total = len(list_servers(k5token).json()['servers'])
    #print list_servers_with_filter(k5token,"status=ACTIVE").json()
    current_active_servers = len(list_servers_with_filter(k5token,"status=ACTIVE").json()['servers'])
    newServers = list_servers_with_filter(k5token,"status=BUILD").json()
    current_errored_servers = len(list_servers_with_filter(k5token,"status=ERROR").json()['servers']) - errorOffset
    duration = (datetime.datetime.strptime(currentts, "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(testResults['testplanbuildstart'], "%Y-%m-%d %H:%M:%S.%f")).total_seconds()
    timeout = testResults['timeout']

    previousas = 0
    previouses = 0
    try:
        while (serverBuildTotal > (current_active_servers + current_errored_servers)) :
            for newserver in list_servers(k5token).json()['servers']:
                for nic in newserver.get('addresses'):
                    if newserver.get('addresses')[nic][0].get('addr') not in serverips:
                        serverips.append(newserver.get('addresses')[nic][0].get('addr'))
                        print "New Server IP Address: ", newserver.get('addresses')[nic][0].get('addr')

            if current_active_servers > 0:

                print "Total requested : ", serverBuildTotal,  "\tActive : ", current_active_servers, "\tError : ", current_errored_servers, "\tAverage : ", duration/current_active_servers
                server['average'] = duration/current_active_servers
                server['activecount'] = current_active_servers
                server['errorcount'] = current_errored_servers
                server['timestamp'] = currentts

            if (previouses != current_errored_servers) or (previousas != current_active_servers):
                testResults['servers'].append(copy.deepcopy(server))


            previousas = current_active_servers
            previouses = current_errored_servers
            current_active_servers = len(list_servers_with_filter(k5token,"status=ACTIVE").json()['servers'])
            current_errored_servers = len(list_servers_with_filter(k5token,"status=ERROR").json()['servers']) - errorOffset
            currentts = str(datetime.datetime.utcnow())
            duration = (datetime.datetime.strptime(currentts, "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(testResults['testplanbuildstart'], "%Y-%m-%d %H:%M:%S.%f")).total_seconds()
            if duration > timeout:
                break

            print "\n\n...waiting for all servers to become ACTIVE or timeout....\n\n"
            # check results every second
            queue9 = Queue()
            sleepp = Process(target=QueuedSleep, args=(queue9, (1)))
            sleepp.start()
            sleepp.join()
    except KeyboardInterrupt:
        pass

    print "Total requested : ", serverBuildTotal,  "\tActive : ", current_active_servers, "\tError : ", current_errored_servers, "\tAverage : ", duration/current_active_servers
    server['activecount'] = current_active_servers
    server['errorcount'] = current_errored_servers
    server['timestamp'] = currentts
    server['average'] = duration/current_active_servers
    testResults['servers'].append(copy.deepcopy(server))

    queue.put(testResults)


def create_demo_security_group(k5token, name):
    """Create a security group

    Args:
        k5token (TYPE): valid K5 token object
        name (TYPE): security group name

    Returns:
        TYPE: a tuple containing  security group name and id
    """
    # Create a new security group
    security_group = create_security_group(k5token, "demosecuritygroup", "Demo Security Group Allows RDP, SSH and ICMP")
    print security_group
    print security_group.json()
    security_group_id = security_group.json()['security_group'].get('id')
    print security_group_id
    security_group_name = security_group.json()['security_group'].get('name')
    # Create security group rules
    # allow rdp
    rdp_rule = create_security_group_rule(k5token, security_group_id, "ingress", "3389", "3389", "tcp")
    print rdp_rule
    print rdp_rule.json()

    # allow ssh # allow rdp
    ssh_rule = create_security_group_rule(k5token, security_group_id, "ingress", "22", "22", "tcp")
    print ssh_rule
    print ssh_rule.json()

    # allow icmp
    icmp_rule = create_security_group_rule(k5token, security_group_id, "ingress", "0", "0", "icmp")
    print icmp_rule
    print icmp_rule.json()
    return (security_group_id, security_group_name)


def create_demo_keypair(k5token, name, publickey, availability_zone):
    """Create a SSH Key Pair

    Args:
        k5token (TYPE): Description
        name (TYPE): Description
        availability_zone (TYPE): Description

    Returns:
        TYPE: Description
    """
    # Create ssh key pair that can be injected into the servers in az1
    server_key = import_keypair(k5token, name, publickey, availability_zone)
    print server_key
    print server_key.json()
    server_key_id = server_key.json()['keypair'].get('id')
    print server_key_id
    server_key_private = server_key.json()['keypair'].get('private_key')
    print server_key_private
    server_key_public = server_key.json()['keypair'].get('public_key')
    print server_key_public
    server_key_name = server_key.json()['keypair'].get('name')
    return (server_key_id, server_key_name, server_key_private, server_key_public)


def create_test_network(k5token, number_of_networks, router_id, availability_zone, cidr_prefix, partial_network):
        """Create the test network infrastructure

        Args:
            k5token (TYPE): valid K5 token object
            number_of_networks (TYPE): number of networks to be created
            router_id (TYPE): the id of the router to be joined to the network
            availability_zone (TYPE): az
            cidr_prefix (TYPE): CIDR prefix
            partial_network (TYPE): boolean - iset True f this is a partial network (i.e. not fully loaded with VMs like the other networks)

        Returns:
            TYPE: Returns a list of all the networks created
        """
        networks = []
        while number_of_networks > 0:
            print "Creating network ", number_of_networks
            networkname = unicode(availability_zone) + unicode("-net-") + unicode(number_of_networks)
            network = create_network(k5token, networkname, availability_zone)
            network_id = network.json()['network'].get('id')
            subnetworkname = unicode(availability_zone) + unicode("-subnet-") + unicode(number_of_networks)
            # assumption that there'll never be more than 100 fully loaded networks
            if partial_network:
                cidr = unicode(cidr_prefix) + unicode("101") + unicode(".0/24")
            else:
                cidr = unicode(cidr_prefix) + unicode(number_of_networks) + unicode(".0/24")
            print "Creating subnet", cidr
            subnet = create_subnet(k5token, subnetworkname, network_id, cidr, availability_zone)
            subnet_id = subnet.json()['subnet'].get('id')
            router_interface = add_interface_to_router(k5token, router_id, subnet_id)
            networks.append([network_id, subnet_id])
            number_of_networks = number_of_networks - 1
        return networks


def get_endpoint(k5token, endpoint_type):
    """Extract the appropriate endpoint URL from the K5 token object body
    Args:
        k5token (TYPE): K5 token object
        endpoint_type (TYPE): trype of endpoint required - e.g. compute, network...

    Returns:
        TYPE: string - contain the endpoint url
    """
    # list the endpoints
    for ep in k5token.json()['token']['catalog']:
        if len(ep['endpoints'])>0:
            # if this is the endpoint that  I'm looking for return the url
            if endpoint_type == ep['endpoints'][0].get('name'):
                #pprint.pprint(ep)
                return ep['endpoints'][0].get('url')


def get_scoped_token(adminUser, adminPassword, contract, projectid, region):
    """Ket a K5 project scoped token

    Args:
        adminUser (TYPE): k5 username
        adminPassword (TYPE): K5 password
        contract (TYPE): K5 contract name
        projectid (TYPE): K5 project id to scope to
        region (TYPE): K5 region

    Returns:
        TYPE: K5 token object
    """
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'

    try:
        response = requests.post(identityURL,
                                 headers={'Content-Type': 'application/json',
                                          'Accept': 'application/json'},
                                 json={"auth":
                                         {"identity":
                                          {"methods": ["password"], "password":
                                           {"user":
                                           {"domain":
                                               {"name": contract},
                                            "name": adminUser,
                                            "password": adminPassword
                                            }}},
                                          "scope":
                                          {"project":
                                           {"id": projectid
                                            }}}})

        return response
    except:
        return 'Regional Project Token Scoping Failure'


def list_servers_with_filter(k5token, filter):
    """Summary - list  K5 projects

    Args:
        k5token (TYPE): valid regional domain scoped token
        filter (TYPE): ACTIVE, ERROR  etc...

    Returns:
        TYPE: http response object
    """
    computeURL = unicode(get_endpoint(k5token, "compute")) + unicode('/servers?') + unicode(filter)
    print computeURL
    token = k5token.headers['X-Subject-Token']
    try:

        response = requests.get(computeURL,
                                headers={
                                     'X-Auth-Token': token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to list servers'


def list_servers(k5token):
    """Summary - list  K5 servers in scoped project token

    Args:
        k5token (TYPE): valid regional domain scoped token

    Returns:
        TYPE: http response object

    """
    computeURL = unicode(get_endpoint(k5token, "compute")) + unicode('/servers/detail')
    print computeURL
    token = k5token.headers['X-Subject-Token']
    try:

        response = requests.get(computeURL,
                                headers={
                                     'X-Auth-Token': token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'})
        return response
    except:
        return 'Failed to list servers'


def create_network(k5token, name, availability_zone):
    """Summary

    Args:
        k5token (TYPE): K5 token object
        name (TYPE): network name
        availability_zone (TYPE): az

    Returns:
        TYPE: http response object
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/networks')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                 headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
                                 json={
                                            "network":
                                            {
                                              "name": name,
                                              "admin_state_up": True,
                                              "availability_zone": availability_zone
                                             }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_subnet(k5token, name, netid, cidr, availability_zone):
    """Create a subnet

    Args:
        k5token (TYPE): token object
        name (TYPE): new subnet name
        netid (TYPE): K5 network id
        cidr (TYPE): CIDR of new subnet
        availability_zone (TYPE): az

    Returns:
        TYPE: http response object
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/subnets')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:

        response = requests.post(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
                                json={
                                             "subnet": {
                                                 "name": name,
                                                 "network_id": netid,
                                                 "ip_version": 4,
                                                 "cidr": cidr,
                                                 "availability_zone": availability_zone
                                             }
                                            })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_router(k5token, name, availability_zone):
    """Create a K5 router

    Args:
        k5token (TYPE): Description
        name (TYPE): Description
        availability_zone (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/routers')
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
                                json={
                                          "router": {
                                               "name": name,
                                               "admin_state_up": True,
                                               "availability_zone": availability_zone
                                          }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def update_router_routes(k5token, routerid, routes):
    """Summary

    Args:
        k5token (TYPE): Descriptionrouter
        routerid (TYPE): Description
        routes (TYPE): Description
        region (TYPE): Description

    Returns:
        TYPE: Description

    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/routers/') + routerid
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.put(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
                                json={"router": {"routes": routes}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def update_router_gateway(k5token, router_id, network_id):
    """Summary

    Args:
        k5token (TYPE): Description
        router_id (TYPE): Description
        network_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/routers/') + router_id
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.put(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
                                json={
                                         "router": {
                                                     "external_gateway_info": {
                                                                                    "network_id": network_id
                                                     }
                                         }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def add_interface_to_router(k5token, router_id, subnet_id):
    """Summary

    Args:
        k5token (TYPE): Description
        router_id (TYPE): Description
        subnet_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/routers/') + router_id + '/add_router_interface'
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.put(networkURL,
                                headers={'X-Auth-Token': token,
                                         'Content-Type': 'application/json'},
                                json={
                                    "subnet_id": subnet_id})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_security_group(k5token, name, description):
    """Summary

    Args:
        k5token (TYPE): Description
        name (TYPE): Description
        description (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/security-groups')
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(networkURL,
                                headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={
                                        "security_group": {
                                            "name": name,
                                            "description": description
                                            }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_security_group_rule(k5token, security_group_id, direction, portmin, portmax, protocol):
    """Summary

    Args:
        k5token (TYPE): Description
        security_group_id (TYPE): Description
        direction (TYPE): Description
        portmin (TYPE): Description
        portmax (TYPE): Description
        protocol (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/security-group-rules')
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(networkURL,
                                headers={'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                json={
                                        "security_group_rule": {
                                            "direction": direction,
                                            "port_range_min": portmin,
                                            "ethertype": "IPv4",
                                            "port_range_max": portmax,
                                            "protocol": protocol,
                                            "security_group_id": security_group_id
                                            }
                                        })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def create_port(k5token, name, network_id, security_group_id, availability_zone):
    """Summary

    Args:
        k5token (TYPE): Description
        name (TYPE): Description
        network_id (TYPE): Description
        security_group_id (TYPE): Description
        availability_zone (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/ports')
    print networkURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(networkURL,
                                 headers={
                                     'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={"port":
                                       {"network_id": network_id,
                                        "name": name,
                                        "admin_state_up": True,
                                        "availability_zone": availability_zone,
                                        "security_groups":
                                        [security_group_id]}})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())


def create_keypair(k5token, keypair_name, availability_zone):
    """Summary

    Args:
        k5token (TYPE): Description
        keypair_name (TYPE): Description
        availability_zone (TYPE): Description

    Returns:
        TYPE: Description
    """
    computeURL = unicode(get_endpoint(k5token, "compute")) + unicode('/os-keypairs')
    print computeURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(computeURL,
                                headers={
                                     'X-Auth-Token': token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'},
                                json={
                                    "keypair": {
                                        "name": keypair_name,
                                        "availability_zone": availability_zone
                                        }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def import_keypair(k5token, keypair_name, publickey, availability_zone):
    """Summary

    Args:
        k5token (TYPE): Description
        keypair_name (TYPE): Description
        availability_zone (TYPE): Description

    Returns:
        TYPE: Description
    """
    computeURL = unicode(get_endpoint(k5token, "compute")) + unicode('/os-keypairs')
    print computeURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(computeURL,
                                headers={
                                     'X-Auth-Token': token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'},
                                json={
                                    "keypair": {
                                        "name": keypair_name,
                                        "public_key": publickey,
                                        "availability_zone": availability_zone
                                        }})
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def create_server_with_port(k5token, name, imageid, flavorid, sshkey_name, security_group_name, availability_zone, volsize,  port_id):
    """Summary

    Args:
        k5token (TYPE): Description
        name (TYPE): Description
        imageid (TYPE): Description
        flavorid (TYPE): Description
        sshkey_name (TYPE): Description
        security_group_name (TYPE): Description
        availability_zone (TYPE): Description
        volsize (TYPE): Description
        port_id (TYPE): Description

    Returns:
        TYPE: Description
    """
    computeURL = unicode(get_endpoint(k5token, "compute")) + unicode('/servers')
    print computeURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(computeURL,
                                headers={'X-Auth-Token':token,'Content-Type': 'application/json','Accept':'application/json'},
                                json={"server": {

                                                 "name": name,
                                                 "security_groups":[{"name": security_group_name }],
                                                 "availability_zone":availability_zone,
                                                 "imageRef": imageid,
                                                 "flavorRef": flavorid,
                                                 "key_name": sshkey_name,
                                                 "block_device_mapping_v2": [{
                                                                               "uuid": imageid,
                                                                               "boot_index": "0",
                                                                               "device_name": "/dev/vda",
                                                                               "source_type": "image",
                                                                               "volume_size": volsize,
                                                                               "destination_type": "volume",
                                                                               "delete_on_termination": True
                                                                            }],
                                                 "networks": [{"port": port_id}],
                                                 "metadata": {"K5 Load Test": "Jumpbox"}
                                                }})

        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def create_jumpbox(k5token, imageid, flavorid, serverkey, security_group, availability_zone, volsize, network, router_id, ext_net):

    # Add external gateway to router (extaz1 is the external network id for one of the external network in availability zone a)
    router_gateway = update_router_gateway(k5token, router_id, ext_net)
    print router_gateway
    print router_gateway.json()

    # Plug new network subnet into the router
    #router_interface = add_interface_to_router(k5token, router_id, network[1])
    #print router_interface
    #print router_interface.json()

    security_group_id = security_group[0]
    print security_group_id
    security_group_name = security_group[1]
    print security_group_name

    name = unicode('jumpbox-') + unicode(availability_zone) +unicode('-') + unicode(randomword(5))

    # Create a new port for the server
    server_port = create_port(k5token, name, network[0], security_group_id, availability_zone)
    print server_port
    print server_port.json()
    server_port_id = server_port.json()['port'].get('id')
    print server_port_id

    server_key_id = serverkey[0]
    print server_key_id
    server_key_public = serverkey[2]
    print server_key_public
    server_key_name = serverkey[1]
    print server_key_name

    # Create the virtual machine
    new_server = create_server_with_port(k5token, name, imageid, flavorid, server_key_name, security_group_name, availability_zone, volsize,  server_port_id)

    print new_server
    print new_server.json()

    # Assign a global/public ip address
    public_ip = create_global_ip(k5token, ext_net, server_port_id, availability_zone)
    print public_ip
    print public_ip.json()
    new_server_public_ip = public_ip.json()['floatingip'].get('floating_ip_address')

    return (new_server_public_ip, server_key_name)


def create_multiple_servers(k5token, name, imageid, flavorid, sshkey_name, security_group_name, availability_zone, volsize,  network_id, max_count):
    """This function will deploy multiple K5 servers with a single K5 API call

    Args:
        k5token (TYPE): K5 token object
        name (TYPE): server base name
        imageid (TYPE): image id of server to be built
        flavorid (TYPE): K5 flavor id to be used (t-shirt size)
        sshkey_name (TYPE): ssh public key name to be injected into the servers (if linux)
        security_group_name (TYPE): K5 security group name
        availability_zone (TYPE): az
        volsize (TYPE): OS disk size in GB
        network_id (TYPE): Network ID where server is to be attached
        max_count (TYPE): Number of servers to be deployed

    Returns:
        TYPE: http response object
    """
    computeURL = unicode(get_endpoint(k5token, "compute")) + unicode('/servers')
    print computeURL
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(computeURL,
                                headers={'X-Auth-Token':token,'Content-Type': 'application/json','Accept':'application/json'},
                                json={"server": {

                                                 "name": name,
                                                 "security_groups":[{"name": security_group_name }],
                                                 "availability_zone":availability_zone,
                                                 "imageRef": imageid,
                                                 "max_count": max_count,
                                                 "return_reservation_id": True,
                                                 "flavorRef": flavorid,
                                                 "key_name": sshkey_name,
                                                 "block_device_mapping_v2": [{
                                                                               "uuid": imageid,
                                                                               "boot_index": "0",
                                                                               "device_name": "/dev/vda",
                                                                               "source_type": "image",
                                                                               "volume_size": volsize,
                                                                               "destination_type": "volume",
                                                                               "delete_on_termination": True
                                                                            }],
                                                 "networks": [{"uuid": network_id}],
                                                 "metadata": {"Example Custom Tag": "Multiple Server Build"}
                                                }})

        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def create_global_ip(k5token, ext_network_id, port_id, availability_zone):
    """Summary

    Args:
        k5token (TYPE): Description
        ext_network_id (TYPE): Description
        port_id (TYPE): Description
        availability_zone (TYPE): Description

    Returns:
        TYPE: Description
    """
    networkURL = unicode(get_endpoint(k5token, "networking")) + unicode('/v2.0/floatingips')
    print networkURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.post(networkURL,
                                headers={
                                     'X-Auth-Token': token,
                                     'Content-Type': 'application/json',
                                     'Accept': 'application/json'},
                                json={
                                             "floatingip": {
                                                     "floating_network_id": ext_network_id,
                                                     "port_id": port_id,
                                                     "availability_zone": availability_zone
                                                     },
                                            })
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

# create a container
def create_new_storage_container(k5token, container_name):
    """
    Create a publically accessible k5 object storage container

    Args:
        container_name (TYPE): Description

    Returns:
        The URL to the new container
    """
    objectURL = unicode(get_endpoint(k5token, "objectstorage")) + '/' + unicode(container_name)
    print objectURL
    token = k5token.headers['X-Subject-Token']

    try:
        response = requests.put(objectURL,
                                 headers={'X-Auth-Token':token,'Content-Type': 'application/json','X-Container-Read': '.r:*'})

        return objectURL
    except:
        return ("\nUnexpected error:", sys.exc_info())

# download item in a container
def download_item_in_storage_container(k5token, container_name, object_name):
    """Download item from K5 object storage

    Args:
        k5token (TYPE): Description
        container_name (TYPE): Description
        object_name (TYPE): Description

    Returns:
        TYPE: Description
    """
    objectURL = unicode(get_endpoint(k5token, "objectstorage")) + '/' + unicode(container_name) + '/' + unicode(object_name)
    print objectURL
    token = k5token.headers['X-Subject-Token']

    response = requests.get(objectURL,
                             headers={'X-Auth-Token':token,'Content-Type': 'application/json'})

    return response

# upload a list to a container
def upload_object_to_container(k5token, container_name, storage_object, object_name):
    """Upload an  object to a K5 container

    Args:
        k5token (TYPE): Description
        container_name (TYPE): Description
        storage_object (TYPE): Description
        object_name (TYPE): Description

    Returns:
        TYPE: Description
    """
    data = storage_object

    objectURL = unicode(get_endpoint(k5token, "objectstorage")) + '/' + unicode(container_name) + '/' + unicode(object_name)
    print objectURL
    token = k5token.headers['X-Subject-Token']

    response = requests.put(objectURL,
                              data=data,
                              headers={'X-Auth-Token':token,'Content-Type': 'application/octet-stream','X-Container-Read': '.r:*'})

    return response


def QueuedSleep(myqueue, mytime):
    time.sleep(mytime)


def BuildAZInfrastructure(k5token, loadednetwork, partialnetwork, routerid, az, cidrprefix, queue):

    if loadednetwork > 0:
        fullnetworklist = create_test_network(k5token, loadednetwork, routerid, az, cidrprefix, False)
    else:
        fullnetworklist = None

    if partialnetwork > 0:
        partialnetworklist = create_test_network(k5token, partialnetwork, routerid, az, cidrprefix, True)
    else:
        partialnetworklist = None

    result = unicode(az) + unicode(' Infrastructure Deployment Complete')
    queue.put((result, fullnetworklist, partialnetworklist))


def DeployAZServers(k5token, fullnetworklist, partialnetworklist, routerid, az, cidrprefix, image_id, flavor_id, ssh_key, security_group, average_server_build_time, partialServerCount, servers_per_network, queue):

    if fullnetworklist is not None:
        for net in fullnetworklist:
            name = unicode("loaded-") + unicode(randomword(5))
            print create_multiple_servers(k5token, name, image_id, flavor_id, ssh_key, security_group, az, 3,  net[0], servers_per_network)
            # delay added to ensure consistent deployment during busy hours - don't overload message queue
            queue6 = Queue()
            sleepp = Process(target=QueuedSleep, args=(queue6, (int(average_server_build_time*servers_per_network))))
            sleepp.start()
            sleepp.join()
    if partialnetworklist is not None:
        for net in partialnetworklist:
            name = unicode("partial-") + unicode(randomword(5))
            print create_multiple_servers(k5token, name, image_id, flavor_id, ssh_key, security_group, az, 3,  net[0], partialServerCount)
            # delay added to ensure consistent deployment during busy hours - don't overload message queue
            queue7 = Queue()
            sleepp = Process(target=QueuedSleep, args=(queue7, (int(average_server_build_time*partialServerCount))))
            sleepp.start()
            sleepp.join()
    result = unicode(az) + unicode(' Server Deployment Complete')
    queue.put(result)


def main():
    """Summary

    Returns:
        TYPE: Description
    """
    global total_servers
    global servers_per_network
    global testAZ1
    global testAZ2
    global buildInfrastructure
    # global
    # global
    # global
    # global
    # global
    # global
    # global


    # Initialise environment parameters
    # adminUser = 'landg' # k5/openstack user login name
    # adminPassword = 'Btbchf1btbyhc!55!' # k5/openstack user password
    # contract = 'YssmW1yI' # k5 contract name or openstack domain name
    # defaultProject = 'YssmW1yI-prj' # default project id - on k5 it's the project name that starts with contract name and ends with -prj
    # extaz1 = 'df8d3f21-75f2-412a-8fd9-29de9b4a4fa8' # K5 availability zone b external network id
    # extaz2 = 'd730db50-0e0c-4790-9972-1f6e2b8c4915' # K5 availability zone b external network id
    # demoProjectA = 'Project_A' # k5/openstack demo target project name
    # demoProjectAid = '7015d1478a4c4bd7b970215d7b0260dd' # k5/openstack demo target project id
    # region = 'uk-1' # target region
    # az1 = 'uk-1a'
    # az2 = 'uk-1b'
    # az1keyname = 'k5-loadtest-az1'
    # az2keyname = 'k5-loadtest-az2'
    # publickey = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAn4+D2gHscLKf2xQMg/kkyNe7DLEO/BG3QYBY0iya298VMSWnHl36fsGLKhhQEmEroauP6+tNt2YgG1ocYEKMoF+Qp4cy1PvU0cSpvRnz/TDYnhx1jlXckzwx4bHmP9rOjMubVICl9Y/o9MUG1BBMTix1XMBw8gSIfvCO/fVSNNyXzSuXApZ+qNug1voNDch4ksdaJaag03FF7yb5HyrKesvcRIwMtohXk1ohowhLJA3NCfvdT3nM4Ct1+YtNX/jmUzhLNOlVsc1EhSWxEpx+yxzdqpTJ/QafY/WkrWO8fiMsDL2FsogjPTPV0JpyKBuv01mxU9Xf2ObW6/QZduaANw== imported-openssh-key'

    # buildInfrastructure = False



    # # parameters for K5 object storage container to hold current results and historical results
    # k5resultcontainer = "K5_Deployment_Results"
    # k5currenttest = "k5current.json"
    # k5testrecords = "k5testrecords.json"
    # k5infracontainer = "K5TestInfrastructure"
    # k5infrafile = "k5testinfra.json"

    # # this is the id of the K5 ubuntu image
    # image_id = "ffa17298-537d-40b2-a848-0a4d22b49df5"
    # # the is the id of a small flavor size (S-2)
    # flavor_id = "1102"

    # # number of servers deploy to region
    # total_servers = 20
    # servers_per_network = 50

    # # delay used to calculate timeouts and set delays between batch API server calls
    # average_server_build_time = 1.61
    # delay necessary for very small test runs under 4 servers
    minimumBuildTime = 240

    # Get a project scoped token
    k5token = get_scoped_token(adminUser, adminPassword, contract, demoProjectAid, region)

    # list used to remove debris from historical runs that don't purge cleanly
    existingProjectservers = []

    # store the infrastructure details for multiple non-destructive runs
    infrastructureDetails = {}


    # ignore historical run data/resources in project
    existing_project_servers = list_servers(k5token).json()['servers']
    print "\n\nExisting Project Servers", existing_project_servers
    for preServer in existing_project_servers:
            existingProjectservers.append(preServer.get('id'))

    # error offset to compensate for existing errors within a project
    errorOffset = len(list_servers_with_filter(k5token,"status=ERROR").json()['servers'])
    print "\n\nExisting Error Count ", errorOffset

    # Toggle for each AZ - when set to True the AZ will be included in the test runs
    # testAZ1 = True
    # testAZ2 = True

    testResults = {"id": None, "timeout": None, "testplantime": None, "averageperserver": None, "testplanbuildstart": None, "testplanbuildfinish": None, "testplanverifystart": None, "testplanverifyfinish": None, "servercount": None, "flavor": None, "image": None, "testplanbuildtime": None, "testplanverifytime": None, "servers": [], "errors": []}

    # calculate the number of servers in each AZ
    if testAZ1:
        az1ServerCount = total_servers/2 + total_servers%2
    else:
        az1ServerCount = 0

    if testAZ2:
        az2ServerCount = total_servers/2
    else:
        az2ServerCount = 0

    # calculate the number of fully loaded networks required  in each az
    #az1fullnetwork = az1ServerCount/servers_per_network
    #az2fullnetwork = az2ServerCount/servers_per_network


    # calculate the number of partially loaded networks
    if az1ServerCount % servers_per_network:
        az1partialnetwork = 1
        az1partialServerCount = az1ServerCount % servers_per_network
    else:
        az1partialnetwork = 0
        az1partialServerCount = 0

    if az2ServerCount % servers_per_network:
        az2partialnetwork = 1
        az2partialServerCount = az2ServerCount % servers_per_network
    else:
        az2partialnetwork = 0
        az2partialServerCount = 0

    total_servers = az1ServerCount + az2ServerCount




    # USING FIXED VALUES RATHER THAN VARIABLES

    # fixed network deployment of 10 networks per AZ based on a maximum of 50 servers per network
    az1fullnetwork = 10
    az2fullnetwork = 10
    az1partialnetwork = 0
    az2partialnetwork = 0
    az1partialServerCount = 0
    az2partialServerCount = 0
    servers_per_network = total_servers/(az1fullnetwork+az2fullnetwork)


    print "\nTotal Servers - ", total_servers
    print "The region will have ", (az1partialnetwork + az2partialnetwork + az1fullnetwork + az2fullnetwork), " networks"
    print "AZ 1 have ", az1fullnetwork, servers_per_network, " node networks and ", az1partialnetwork, " network with ", az1partialServerCount, " servers"
    print "AZ 2 have ", az2fullnetwork, servers_per_network," node networks and ", az2partialnetwork, " network with ", az2partialServerCount, " servers\n"




    if not buildInfrastructure:
        # use existing infrastructure
        # download the previous run infrastructure details
        try:
            infrastructureDetails = download_item_in_storage_container(k5token, k5infracontainer, k5infrafile).json()
        except:
            # if this is the first run then create the K5 infrastructure first
            print "No infrastructure file available - please ensure to build out the K5 infrastructure first."
            print "Set the 'buildInfrastructure' toggle to True on the first run of this script"
            sys.exit(0)
        az1infra = infrastructureDetails['az1infra']
        az2infra = infrastructureDetails['az2infra']
        az1Router_id =infrastructureDetails['az1RouterId']
        az2Router_id = infrastructureDetails['az2RouterId']
        az1_ssh_key_pair = infrastructureDetails['az1SSHKP']
        az2_ssh_key_pair = infrastructureDetails['az2SSHKP']
        security_group = infrastructureDetails['SecurityGroup']
        JumpBox = infrastructureDetails['jumpbox']

    else:
        # build out  infrastructure
        # create router in az1 to link all networks
        if testAZ1:
            az1Router = create_router(k5token, "az1Router", "uk-1a")
            az1Router_id = az1Router.json()['router'].get('id')
            print "AZ1 Router ID -> ", az1Router_id
            infrastructureDetails['az1RouterId'] = az1Router_id
            az1_ssh_key_pair = create_demo_keypair(k5token, az1keyname, publickey, az1)
            print "AZ1 SSH Key Pair > \n", az1_ssh_key_pair
            infrastructureDetails['az1SSHKP'] = az1_ssh_key_pair

        # create router in az2 to link all networks
        if testAZ2:
            az2Router = create_router(k5token, "az2Router", "uk-1b")
            az2Router_id = az2Router.json()['router'].get('id')
            print "AZ2 Router ID -> ", az2Router_id
            infrastructureDetails['az2RouterId'] = az2Router_id
            az2_ssh_key_pair = create_demo_keypair(k5token, az2keyname, publickey, az2)
            print "AZ2 SSH Key Pair > \n", az2_ssh_key_pair
            infrastructureDetails['az2SSHKP'] = az2_ssh_key_pair

        security_group = create_demo_security_group(k5token, "loadtest")
        print "Security Group > ", security_group
        infrastructureDetails['SecurityGroup'] = security_group

        az1cidrPrefix = "192.168."
        az2cidrPrefix = "10.10."


        queue2 = Queue()
        p2 = Process(target=BuildAZInfrastructure, args=(k5token, az1fullnetwork, az1partialnetwork, az1Router_id, az1, az1cidrPrefix, queue2))
        p2.start()

        queue3 = Queue()
        p3 = Process(target=BuildAZInfrastructure, args=(k5token, az2fullnetwork, az2partialnetwork, az2Router_id, az2, az2cidrPrefix, queue3))
        p3.start()

        # wait here until all the servers have been deployed - each AZ is deployed using a separate thread
        p2.join()
        p3.join()

        az1infra = queue2.get()
        az2infra = queue3.get()

        print az1infra[0], az1infra
        infrastructureDetails['az1infra'] = az1infra
        print az2infra[0], az2infra
        infrastructureDetails['az2infra'] = az2infra


        # Create inter az  network connections
        print "creating a network connector"
        routerLinks =  create_inter_az_link(k5token, demoProjectAid, az1infra[1], az2infra[1], az1, az2,  security_group[0])

        print routerLinks

        # adding cross AZ routing - using /16 cidr to allow all /24 cidrs
        az1dest = unicode(az1cidrPrefix) + unicode('0.0/16')
        az2dest = unicode(az2cidrPrefix) + unicode('0.0/16')

        RoutesAZ1 = [{'destination': az2dest, 'nexthop': routerLinks[0][2][0]}]
        RoutesAZ2 = [{'destination': az1dest, 'nexthop': routerLinks[1][2][0]}]

        print "AZ1 ROUTES - ", RoutesAZ1
        print "AZ2 ROUTES - ", RoutesAZ2

        print update_router_routes(k5token, az1Router_id, RoutesAZ1).json()
        print update_router_routes(k5token, az2Router_id, RoutesAZ2).json()

        # create jump box for management
        JumpBox = create_jumpbox(k5token, image_id, flavor_id, az1_ssh_key_pair, security_group, az1, 10, az1infra[1][0],  az1Router_id, extaz1)

        infrastructureDetails['jumpbox'] = JumpBox



        # convert them back to JSON for upload to storage container
        infrastructureDetails = json.dumps(infrastructureDetails)

        # upload results
        result = create_new_storage_container(k5token, k5infracontainer)
        infraresult = upload_object_to_container(k5token, k5infracontainer, infrastructureDetails, k5infrafile)
        print "^^^^^^ Navigate to this URL to locate current infrastructure settings ^^^^^^^\n\n"

    # start monitoring service

    testResults['id'] = str(datetime.datetime.utcnow())

    # if the testing goes beyond this time then something has gone wrong with the K5 deployment
    timeout = ((total_servers * average_server_build_time) * 1.1) + minimumBuildTime

    # capture data in results file
    testResults['servercount'] = total_servers
    testResults['timeout'] = timeout
    testResults['flavor'] = flavor_id
    testResults['image'] = image_id
    testResults['testplanbuildstart'] = str(datetime.datetime.utcnow())

    queue = Queue()
    p = Process(target=verify_servers_active, args=(queue, k5token, testResults, errorOffset))
    p.start()
    startMonitoring = str(datetime.datetime.utcnow())

    # start the server deployment


    queue12 = Queue()
    p12 = Process(target=DeployAZServers, args=(k5token, az1infra[1], az1infra[2], az1Router_id, az1, "192.168.", image_id, flavor_id, az1_ssh_key_pair[1], security_group[1], average_server_build_time, az1partialServerCount, servers_per_network, queue12))
    p12.start()

    queue13 = Queue()
    p13 = Process(target=DeployAZServers, args=(k5token, az2infra[1], az2infra[2], az2Router_id, az2, "10.10.", image_id, flavor_id, az2_ssh_key_pair[1], security_group[1], average_server_build_time, az2partialServerCount, servers_per_network, queue13))
    p13.start()

    # wait here until all the servers have been deployed - each AZ is deployed using a separate thread
    p12.join()
    p13.join()

    print queue12.get()
    print queue13.get()



    print "\n\n\n\nFinished all server BUILDS \n\n\n"
    print "\n\n...waiting for all servers to become ACTIVE....\n\n"

    # wait for all servers to be verified active before proceeding - running inseparate thread
    p.join()

    testResults = queue.get()
    print testResults
    testResults['testplanverifystart'] = startMonitoring
    testResults['testplanbuildfinish'] = str(datetime.datetime.utcnow())
    testResults['testplanbuildtime'] = (datetime.datetime.strptime(testResults['testplanbuildfinish'], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(testResults['testplanbuildstart'], "%Y-%m-%d %H:%M:%S.%f")).total_seconds()

    testResults['testplanverifyfinish'] = str(datetime.datetime.utcnow())
    testResults['testplanverifytime'] = (datetime.datetime.strptime(testResults['testplanverifyfinish'], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(testResults['testplanverifystart'], "%Y-%m-%d %H:%M:%S.%f")).total_seconds()
    testResults['testplantime'] = (datetime.datetime.strptime(testResults['testplanverifyfinish'], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(testResults['testplanbuildstart'], "%Y-%m-%d %H:%M:%S.%f")).total_seconds()

    # calculate average build time for active servers
    current_active_servers = len(list_servers_with_filter(k5token,"status=ACTIVE").json()['servers'])
    testResults['averageperserver'] = testResults['testplantime']/current_active_servers

    # capture all the new errors in the log file
    current_servers = list_servers(k5token).json()['servers']
    print "\n\nLATEST SERVERS LIST\n\n", current_servers

    print "\n\nExisting Server List\n\n", existingProjectservers
    for new_server in current_servers:
        if new_server.get('status') != 'ACTIVE':
            if new_server.get('id') not in existingProjectservers:
                print "\n\nAddind new errored server\n", new_server
                testResults['errors'].append(copy.deepcopy(new_server))

    # download the previous set of results from k5 object storage so that the current results can be appended and re-uploaded
    try:
        #result = download_item_in_storage_container(k5tokenA, demoProjectAid, k5resultcontainer, k5testrecords, region).json()
        storedResults = download_item_in_storage_container(k5token, k5resultcontainer, k5testrecords).json()
    except:
        # if this is the first run the create the K5 object storage container
        print "Creating new object storage container for results"
        result = create_new_storage_container(k5token, k5resultcontainer)
        storedResults = []

    # append current results to historical test results
    storedResults.append(testResults)

    # convert them back to JSON for upload to storage container
    currentResults = json.dumps(testResults)
    storedResults = json.dumps(storedResults)

    print "AZ1 SSH Key Pair > \n", az1_ssh_key_pair, "\n", az1_ssh_key_pair[2]
    print "AZ2 SSH Key Pair > \n", az2_ssh_key_pair, "\n", az2_ssh_key_pair[2]

    # upload results
    result = upload_object_to_container(k5token, k5resultcontainer, storedResults, k5testrecords)
    print "^^^^^^ Navigate to this URL to locate current and historical test run results ^^^^^^^\n\n"
    result = upload_object_to_container(k5token, k5resultcontainer, currentResults, k5currenttest)
    print "^^^^^^ Navigate to this URL to locate current test run results ^^^^^^^"
    print "\nJumpbox Details --> ", unicode(JumpBox)



if __name__ == "__main__":
    main()
