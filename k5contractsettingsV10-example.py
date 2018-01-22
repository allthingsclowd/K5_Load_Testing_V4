#!/usr/bin/python

# Enter K5 Contract details
adminUser = 'username' # k5/openstack user login name
adminPassword = 'password' # k5/openstack user password
contract = 'contract name' # k5 contract name or openstack domain name
contractid = 'contractid'
defaultid = 'default project id'
defaultProject = 'default project name' # default project id - on k5 it's the project name that starts with contract name and ends with -prj
region = 'uk-1' # target region
az1 = 'uk-1a'
az2 = 'uk-1b'

# K5 external network details
extaz1 = 'df8d3f21-75f2-412a-8fd9-29de9b4a4fa8' # K5 availability zone b external network id
extaz2 = 'd730db50-0e0c-4790-9972-1f6e2b8c4915' # K5 availability zone b external network id

# K5 target Project
demoProjectA = 'Project Name' # k5/openstack demo target project name
demoProjectAid = 'Project ID' # k5/openstack demo target project id

# APPLICATION DETAILS

# Enter total number of servers to deploy to region
total_servers = 20

# Enter SSH Key names - must be unique per az
az1keyname = 'k5-loadtest-az1'
az2keyname = 'k5-loadtest-az2'
# Public Key to use - does not need to be unique
publickey = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAn4+D2gHscLKf2xQMg/kkyNe7DLEO/BG3QYBY0iya298VMSWnHl36fsGLKhhQEmEroauP6+tNt2YgG1ocYEKMoF+Qp4cy1PvU0cSpvRnz/TDYnhx1jlXckzwx4bHmP9rOjMubVICl9Y/o9MUG1BBMTix1XMBw8gSIfvCO/fVSNNyXzSuXApZ+qNug1voNDch4ksdaJaag03FF7yb5HyrKesvcRIwMtohXk1ohowhLJA3NCfvdT3nM4Ct1+YtNX/jmUzhLNOlVsc1EhSWxEpx+yxzdqpTJ/QafY/WkrWO8fiMsDL2FsogjPTPV0JpyKBuv01mxU9Xf2ObW6/QZduaANw== imported-openssh-key'

# Toggle  - False will result in only the test servers being destroyed or recreated
#              - True will result in ALL infrastructure being redeployed or destroyed
buildInfrastructure = False

# parameters for K5 object storage container to hold current results and historical results
k5resultcontainer = "K5_Deployment_Results"
k5currenttest = "k5current.json"
k5testrecords = "k5testrecords.json"
k5infracontainer = "K5TestInfrastructure"
k5infrafile = "k5testinfra.json"

# this is the id of the K5 ubuntu image
image_id = "ffa17298-537d-40b2-a848-0a4d22b49df5"

# the is the id of a small flavor size (S-2)
flavor_id = "1102"

# delay used to calculate timeouts and set delays between batch API server calls
average_server_build_time = 1.61

# Toggle for each AZ - when set to True the AZ will be included in the test runs
testAZ1 = True
testAZ2 = True

# unused - please don't change - to be worked on later
servers_per_network = 10

