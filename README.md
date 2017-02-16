# K5_Load_Testing Script

## Building Mode
# launch_servers.py
This program has two roles :

- Infrastructure Deployment

Build out a K5 region wide infrastructure, both datacentres az1 and az2, capable of hosting 1000VMs (only tested to 1000 could potentially go beyond). All 1000 VMs within this region will be capable of communicating with each other over the K5 intranet. No internet traffic required.
Note: Speak with your Fujitsu K5 contract owner if you need to test beyond the quotas set by default within a project (20 virtual machines at the time of writing this ReadMe). The script was tested up to 2000 vCPU. The quotas within projects are soft limits that can be changed by K5 administrators. A Jumpbox server is also deployed and the public ip address provided once the initial script run completes.

- Test Server Deployment

When the infrastructure is deployed the script starts a background monitoring process which will be used to time all the test server deployments.
The servers are then deployed in batches sizes of (total servers/number of networks[defaults to 20]) and a delay of (1.61*batch size)  seconds is invoked before deploying the next batch. This process is run in parallel across both availability zones.

## Configuration File - k5contractsettingsV10.py
Before launching either of the scripts in this repo it is necessary to first configure all sections of the k5contractsettingsV10.py file with K5 contract details, ssh keys to use, target project etc.

## total_servers = 20 <---- Ensure to set this to meet your needs

## 'buildInfrastructure' toggle
After the initial run of this script it is necessary to toggle the 'buildInfrastructure = True' to 'buildInfrastructure = False' in the k5contractsettingsV10.py file.
This ensures that subsequent test runs leverage the existing infrastructure - the configuration details are stored in K5's object storage during deployment and simply read back in on subsequent test runs.
The same toggle is used to ensure that the purge_project_parallel.py file only purges the servers under test.

The script builds and configures the necessary infrastructure (security groups, networks subnets etc) for half the total server count in each K5 availability zone within the region under test. It then links ALL the subnets to ensure all nodes can communicate with each other. A Jumpbox server is also deployed and the public ip address provided once the initial script completes.

## Operation post Infrastructure Deployment
Before the script starts deploying the servers, which is done in parallel queues, it also launches a routine to time & monitor the state of the deploying servers in the background. As soon as a new server ip address is detected this is sent to standard output. When a server becomes ACTIVE or ERROR state this is also presented back to standard output.
When the servers are all deployed the monitoring routing will continue giving a progress update to standard output until all servers have been accounted for (deployed/errored/timed out).

## Output of Results
During deployment and testing all API endpoints called are printed to standard output for reference.
Once all servers are active the monitoring script terminates and the results are logged into two files:
- 1. current results
- 2. historical results

Both of these files are then uploaded to the K5 container object specified in the container settings of the k5contractsettingsV10.py file.

After the initial run to build out the test infrastructure ensure to toggle the 'buildinfrastructure' to false in the k5contractsettingsV10.py file. All subsequent builds and purges will only affect the servers being tested.

## How to launch the script
python launch_servers.py

## Destroying Mode
# purge_project.py
This program will obliterate everything in your project...be warned!!!!
Updates: toggle the 'buildinfrastructure' to false in the k5contractsettingsV10.py file to keep the infrastructure and only purge the servers under test.
Adjust the KeyPair and Security Group purge sections to meet your needs.
This file imports the following to files:
- 1. k5contractsettingsV10.py - the credentials and environmental settings need to be configured here
- 2. k5APIwrappersV19.py - api library file

##Note : Further debugging is required as often it requires 2 or 3 runs to purge the project completely - runs in parallel and can saturate some wifi routers!!!!

## How to launch the script
python purge_project.py


