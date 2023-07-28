# Data Engineering using 

# AWS Analytics Services

**Sections 17 - 21**



## Section 17 - Getting Started with AWS EMR

Common use case for EMR Cluster: Data Engineering, BI or Ad-hoc querying

EMR: cloud big data platform to run large-scale distributed data processing jobs, interactive SQL quieries, and ML applications wirh analytics frameworks like Apache Spark, Apache Hive, Presto, ...

- schedule and run data engineering jobs with tools like AirFlow
- Connect BI Tools for reporting using Spark JDBC Connector
- Run Ad-hoc queries using Spark SQL leveraging Jupyter environment
- need to determine EMR components necessary to set up cluster
- use auto-scaling features provided by AWS EMR for cost control

**Create new key pair**

- go to EC2 and create new key pair
- download key file and adjust read/write permissions: ``chmod 600 [key file name]``

**Set Up EMR Cluster with Spark**

- set up EMR cluster with advanced options
- create cluster with Hadoop and Spark
- use spark for meta data glue catalog tables
- select instance groups instead of instance fleets
- configure EMR-managed scaling
- use default values for most settings
- start cluster, overview/ summary page gives information about the cluster including primary node public DNS
- once cluster is up and running, can get information and address for all applications on primary and core/ task nodes
- can monitor on cluster, node or I/O level
- for trouble shooting, check metrics and configuration properties
- events log information like starting cluster, all steps in the order of execution, resizing of groups, ...
- can configure steps (also after starting cluster), upload .jar file, streaming application, ..., can give runtime arguments and specify behavior on failure
- can create bootstrap action to run on condition or custom action, need to provide script location for bootstrap action, use bootstrapping to install prerequisites required for applications to run on cluster

**Connect to Master node**

- use ssh to connect to master node, user name hadoop, public DNS as provided
- hadoop is super user, can run all normal linux commands
- leave hadoop cluster by typing ``exit``

**Terminate Cluster**

- to terminate cluster, first need to remove termination protection
- works from web console and CLI
- termination protection to prevent accidental termination

**Clone Cluster**

- can clone terminated or active cluster to create a new cluster with same configuration
- cloning opens *create cluster* interface with all settings/properties from cloned cluster preselected, can be changed

**Listing and Managing Files in S3 from EMR Cluster**

- log into master node using ssh
- AWS CLI is preconfigured on master node
- from hadoop, list all folders in itv github bucket: ``aws s3 ls s3://[bucket name]``
- can list buckets and files from master node
- list files from HDFS CLI: ``hadoop [fs/ hdfs/ dfs] -ls``, gives files/ folders from HDFS location
- list objects in bucket through HDFS: ``hdfs dfs -ls s3://[bucket name]``
- download new github activity data on HDFS and then move the data to S3
- create new directory and download github activity data for next day into the folder
- copy all files from the directory to S3: ``hdfs dfs --copyFromLocal * s3://[bucket name]``
- delete files from S3 through HDFS: ``hdfs dfs -rm s3://[bucket name]/landing/ghactivity/2021-01-17*``



## Section 18 - Deploying Spark Application using AWS EMR

