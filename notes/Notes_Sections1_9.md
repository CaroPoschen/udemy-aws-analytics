# Data Engineering using AWS Analytics Services

**Sections 1 - 9**



## Section 2 - Setup Local Development Environment for AWS on Windows

``wsl`` windows system for Linux? set up local Linux system on my windows machine

#### Shell Scripting

- ``aws configure`` configure default AWS profile in CLI
- ``aws configure --profile [profile name]`` configure specific AWS profile, reference IAM user from account
- *.aws/credentials* hidden folder where access key and secret key for profiles is saved
- ``aws s3 ls`` list all S3 buckets associated with the default profile
- ``aws s3 ls --profile [profile name]`` list all S3 buckets associated with the given profile
- ``python3 -m venv [environment name]`` use module *venv* to create a virtual python environment in the current folder with the given name
- ``source [oenvironment name]/bin/activate`` activate created virtual python environment
- ``pip install [module]`` install module using *pip* - python package installer
- ``pip install  jupyterlab`` install module to use jupyter notebooks in current environment
- ``jupyter lab`` create link to jupyter environment, provides URL with secret token to connect notebook to the current environment, keeps all settings defined in CLI



## Section 4 - Cloud 9

Cloud9: IDE connected to one EC2 instance, set up 

Terminal commands:

- ``docker ps`` check for any docker container on the machine
- ``docker ps -a`` list all created docker containers on the machine
- `` sudo systemctl status docker`` check system status for docker
- validate programming languages on machine
  - Python: type ``python`` in terminal and press tab to see all available commands - and python versions - starting with *python*
  - ``java -version`` and ``javac -version`` to check for available Java versions
- ``df -h`` file system sizes, can check EBS size here, can increase in GUI, need to reboot after changing EBS size
- adjust security group to open port for cloud9

**Jupyter Lab from Cloud9**

- make sure python 3 is installed
- create folder for project and go there
- use ``python3 -m venv [environment name]`` to create virtual environment
- run ``source [environment name]/bin/activate`` to activate the environment (have environment name in parenthesis in front of user name to show that environment is active)
- install jupyterlab in the environment ``pip install jupyterlab``
- start webserver ``jupyter lab --ip 0.0.0.0``
  - for issues with versions of *urllib* and *OpenSSL* use ``pip install urllib3==1.26.6 ``
- open port for jupyter lab instance (8888 default) in security group
- run jupyter lab in the background ``nohup jupyter lab --ip 0.0.0.0 & ``
  - run ``tail nohup.out`` to get token printed in console



## Section 5 - AWS Getting Started with S3, IAM, and CLI

build a data lake on top of S3, for that create S3 bucket and create two folders, *landing* and *raw*

- *landing* is the first landing spot for the data, in this case JSON, ingest data from external sources
- *raw* is the storage part of the date in the desired format of the data lake

IAM

- create user group to attach policies to, so all users for this project have the necessary policies
- create custom policy to give full access to just the created S3 bucket, and attach to the group
- in AWS CLI setup the profile by running ``aws configure --profile [profile  name]`` and enter access key and secret key from AWS user



## Section 6 - Storage - Deep Dive into AWS S3

- clone github [project](https://github.com/dgadiraju/retail_db) locally and the upload data into new S3 bucket

- enable version control for bucket and add lifecycle rule to delete files with custom prefix after 3 days

- create a new S3 bucket in a different region for cross-region replication, based on specific prefix

  - use new IAM role with AWSS3FullAccess policy for replication
  - in original bucket, add replication rule, give new bucket (in different region) and provide new IAM role

- different S3 types for for different usages, can change storage class for new or uploaded files, or for replication rule

- change life cycle rule and replication rule for replication bucket to use storage class glacier

- important S3 CLI commands: ``aws s3``

  - ``ls`` list objects and folders
  - ``cp`` copy files
  - ``mv`` move objects and folders
  - ``rm`` delete objects and folders
  - ``mb`` create bucket
  - ``rb`` remove bucket

- can add other options to arguments, example:

  ```
      aws s3 cp ~/Research/data/retail_db s3://dg-retail1/retail_db/ \
       --recursive \
       --exclude "*.sql" \
       --exclude "README.md" \
       --profile itvsupport1
  ```





## Section 7 - AWS Security using IAM

##### IAM Policies

- set of permissions in JSON syntax
- assigned to groups, roles or users (IAM identities), can have more than one policy per identity
- predefined policies or define custom ones
- policy terms:
  - *Effect* typically 'Allow' or 'Deny'
  - *Action* type of actions to have described effect
  - *Resource* control resources that are related to the Effect
  - *\** Wildcard
- usually have users in groups (one or more) and assign policies to groups (users inherit policies from groups)
- can assign permission on fine grains (i.e. all resources of a type, one specific resource or one part of a resource, like just one folder in one S3 bucket)

##### IAM Roles

- roles are associated to services, attach policies to roles, which will be inherited by services
- select service to create the role for

##### Managing IAM using CLI

Examples

```shell
aws iam list-users --profile itvadmin
aws iam list-groups --profile itvadmin
aws iam list-roles --profile itvadmin
 
# Lists all AWS Managed Policies as well as custom policies
aws iam list-policies --profile itvadmin
 
# List only custom policies
aws iam list-policies --scope Local --profile itvadmin



aws iam create-user --user-name itvsupport2 --profile itvadmin
aws iam list-users --profile itvadmin
     
aws iam add-user-to-group \
 --group-name itvsupport \
 --user-name itvsupport2 \
 --profile itvadmin
     
aws iam list-groups-for-user \
 --user-name itvsupport2 \
 --profile itvadmin

aws iam remove-user-from-group \
 --group-name itvsupport \
 --user-name itvsupport2 \
 --profile itvadmin
aws iam delete-user \
 --user-name itvsupport2 \
 --profile itvadmin
```



## Section 8 - Infrastructure - Getting Started with EC2

- different types, optimized for different use cases
- ``hostname -f`` provides host name
- ``uname -a`` get name and kernel details
- should have a key pair to connect to an instance
- connect to EC2 via ssh if port 22 is open in security rule
- instances have a private IP address, used for communication within AWS
- can have public IP address for communication with other services/ internet outside AWS
- instances can be running, stopped or starting, terminating will kill the instance, may have to keep paying for EBS if instance is stopped, depending on settings
- can allocate an elastic IP address and associate it to a service, that way, public IP address will not change, even if service is stopped and restarted

**AWS EC2 CLI**

- getting help ``aws ec2 help``

- describe instances

  ```shell
  aws ec2 describe-instances \
    --profile itvadmin \
    --region us-west-1
       
  aws ec2 describe-instances \
    --profile itvadmin \
    --region us-west-1 | \
    grep -i instanceid
       
  # You can use one of the instance ids and get instance status
  aws ec2 describe-instance-status \
    --instance-id i-07c085b765f162233 \
    --profile itvadmin \
    --region us-west-1
  ```

- stop instance

  ```shell
  aws ec2 stop-instances \
    --instance-id i-07c085b765f162233 \
    --profile itvadmin \
    --region us-west-1
       
  aws ec2 describe-instance-status \
    --instance-id i-07c085b765f162233 \
    --profile itvadmin \
    --region us-west-1
  ```

- start instance

  ```shell
  aws ec2 start-instances \
    --instance-id i-07c085b765f162233 i-00f80143dc2e77b85 \
    --profile itvadmin \
    --region us-west-1
       
  aws ec2 describe-instance-status \
    --instance-id i-07c085b765f162233 i-00f80143dc2e77b85 \
    --profile itvadmin \
    --region us-west-1
  ```

- list allocated elastic IPs

  ```shell
  aws ec2 describe-addresses \
    --profile itvadmin \
    --region us-west-1
  ```

**Upgrade/ Downgrade Instance**

- can increase/ decrease memory or CPU of an instance when it is stopped

- vertical scaling

- confirm memory of current machine in CLI ``free -h``

- confirm CPU config of current machine in CLI ``lscpu``

- change instance type in CLI

  ```shell
  aws ec2 stop-instances \
    --instance-id i-07c085b765f162233 \
    --profile itvadmin \
    --region us-west-1
       
  aws ec2 modify-instance-attribute \
    --instance-id i-07c085b765f162233 \
    --instance-type t2.micro \
     --profile itvadmin \
     --region us-west-1
       
  aws ec2 describe-instances \
    --instance-id i-07c085b765f162233 \
     --profile itvadmin \
     --region us-west-1
       
  aws ec2 start-instances \
    --instance-id i-07c085b765f162233 \
    --profile itvadmin \
    --region us-west-1
  ```

  

## Section 9 - Infrastructure - EC2 Advanced

- instances have a lot of metadata describing the instace

  ```shell
  aws ec2 describe-instances \
    --profile itvadmin \
    --region us-west-1 > instances.json
  ```

- can use options *query* and *filter* get get only specific information for specific instances

  ```shell
  aws ec2 describe-instances \
     --query 'Reservations[*].Instances[*].{Instance:InstanceId,Status:State.Name}' \
     --output json \
     --profile itvadmin \
     --region us-west-1
  ```

  ```shell
  aws ec2 describe-instances \
    --filters Name=instance-type,Values=t2.micro \
    --output json \
    --profile itvadmin \
    --region us-west-1
  
  aws ec2 describe-instances \
    --filters Name=instance-type,Values=t2.micro \
    --query 'Reservations[*].Instances[*].{Instance:InstanceId,InstanceType:InstanceType,Status:State.Name}' \
    --output json \
    --profile itvadmin \
    --region us-west-1
  
  aws ec2 describe-instances \
    --filters Name=instance-type,Values=t2.micro Name=instance-state-name,Values=stopped \
    --query 'Reservations[*].Instances[*].{Instance:InstanceId,InstanceType:InstanceType,Status:State.Name}' \
    --output json \
    --profile itvadmin \
    --region us-west-1
  ```

- can provide script when launching instance under *user data* to run a bootstrap script that will run on initiating to install packages...

  ```shell
  #!/bin/bash
  apt update -y
  apt install apache2 -y
  apt install python3-pip -y
  python3 -m pip install awscli
  ```

  ```shell
  aws ec2 run-instances \
     --image-id ami-013f17f36f8b1fefb \
     --count 1 \
     --instance-type t2.micro \
     --key-name keyname \
     --security-group-ids sg-ID \
     --user-data file://ec2_user_data.sh
  ```

- when instance is up and completely setup, can create an AMI from that instance to launch more instances with that setup

  - create snapshot of instance

  - build AMI from that snapshot

    ```shell
    aws ec2 create-image \
       --instance-id i-ID \
       --name webAppAMI \
       --description "A sample AMI with pre installed apache web server"
    ```

  - launch new instance with newly created AMI

    ```shell
    aws ec2 run-instances \
      --image-id ami-ID \
      --count 1 \
      --instance-type t2.micro \
      --key-name keyname \
      --security-group-ids sg-ID
    ```

    

  
