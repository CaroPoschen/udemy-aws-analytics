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

- can only use notebooks on top of EMR clusters that were deployed using IAM user, not for EMR clusters provisioned by the root account
- set up EMR cluster
  - use spark, hadoop and JupyterEnterpriseGateway
  - use spark for metadata
  - choose minimal number of instances for cluster
  - set auto-termination to 30min
  - leave other settings to default
  - start cluster
- create EMR Workspace (formerly Notebook) on EMR cluster, need to have sufficient permissions
- log into master node using SSH
- check that AWS CLI is installed by running a test command: ``aws s3 ls s3://[bucket name]``
- list all files in current directory using HDFS: ``hdfs dfs -ls /``

**Set up EMR Workspace (formerly Notebook)**

- to create Studio Workspace in new Environment, fist need to set up studio
  - name
  - VPC and Subnets, all need to be tagged with key **for-use-with-amazon-emr-managed-policies** and value **true**
  - need to specify a S3 bucket for the workspace(ideally new bucket)
  - needs IAM role, that has permissions on the workspace bucket
- Select newly created studio and then create workspace
- set up most properties when creating studio, little setup for workspace itself
- start workspace
- launch workspace, can open either as JupyterLab or Jupyter interface, example uses JupyterLab
- select Kernel and run example command to test Jupyter environment on top of cluster

**Add data to EMR S3 bucket**

- create folder to localy download data: ``mkdir -p ~/Downloads/ghactivity``

- download ghactivity data for Jan 13, 2021 as above

- upload data from local folder to s3 bucket, make sure to only upload data for specific date

  ```shell
  aws s3 \
  > cp . s3://itv-emr-studio/itv-emr-studio/prod/landing/ghactivity/ \
  > --exclude "*" \
  > --include "2021-01-13*" \
  > --recursive
  ```

- validate upload: ``aws s3 ls s3://itv-emr-studio/itv-emr-studio/prod/landing/ghactivity/``

- download and upload data for next two days as well as described here

**Validate Application for EMR Cluster**

- use previous Python program
- check Spark and Python version on cluster, and make sure that versions match for both on PySpark application and on cluster
- may need to delete virtual environment folders and recreate it using matching python version
- install correct version of spark: ``pip install pyspark==3.4.0``
- list all relevant python files in folder: ``ls -ltr *.py``: *process, read, util, write*
- create zip file with these programs (Linux): ``zip [folder name].zip *.py``

**Deploy Application on EMR Master Node**

usually use step execution, will cover that later

- copy zip file to master node: `` scp -i ~/aws-itv-keypair.pem /mnt/c/Caro/AWS/Udemy/udemy-aws-analytics/project/pyspark-demo/itv-ghactivity.zip hadoop@[master node DNS]:~``
- create *gh-activity* folder on master node and move zip file there, also copy *app.py* program there using *scp*

**Validate that user is capable of running PySpark applications on cluster**

- to check, just run ``pyspark`` in master node console
- if it fails, double check video 266, may have wrong user details (currently logged in as hadoop user, who owns *hdfsadmingroup* on master node and therefor has all necessary rights)
- if it fails
  - run command ``sudo -u hdfs hdfs dfs -mkdir /user/[current user name]``
  - check permissions on folders, that current user owns the new folder
  - if user does not own folder: ``sudo -u hdfs hdfs dfs -chown -R [user name]:[user name] /user/[user name]``
  - if current user owns folder under /user, can then launch pyspark without issues

**Run Spark Session using spark-submit**

- need to set life cycle environment variables

  - ``export ENVIRON=PROD``
  - ``export SRC_DIR=s3://itv-emr-studio/itv-emr-studio/prod/landing/ghactivity/``
  - ``export SRC_FILE_FORMAT=json``
  - ``export TGT_DIR=s3://itv-emr-studio/itv-emr-studio/prod/raw/ghactivity/``
  - ``export TGT_FILE_FORMAT=parquet``
  - review all environment variables: ``env``
  - ``export SRC_FILE_PATTERN=2021-01-13``

- start application using spark submit:

  ```shell
  spark-submit \
    --master yarn \ (optional on EMR because default)
    --py-files itv-ghactivity.zip \
    app.py
  ```

- make sure that workers have enough resources to run application

- once finished in console, validate that files are in correct format in the correct location: ``aws s3 ls s3://itv-emr-studio/itv-emr-studio/prod/raw/ghactivity/ --recursive``

**Validate data using Jupyter notebook environment**

- open notebook created earlier
- make sure to have pyspark as kernel
- run commands in notebook, so far validate only for one day, as only one day ran so far
- also adjust environment variables and run spark job for 2021-01-14 and 2021-01-15
- once data for additional dates is processed, run commands in notebook again to check the counts and counts for different dates

**Delete Data from target folder to reuse same dates using different approach**

- delete all data in folder using console ``aws s3 rm s3://itv-emr-studio/itv-emr-studio/prod/raw/ghactivity/ --recursive``

**Differences between Spark Client and Cluster Deployment**

- for ``spark-submit``, have options ``client``( default) and ``cluster`` for ``deploy-mode``

- environment variables are set locally, but job will run on cluster, so are not seen by worker nodes

- to run spark-submit in cluster node, need to parse environment variables in a particular syntax

  ```shell
  spark-submit \
    --master yarn \
    --deploy-mode cluster \
    --conf "spark.yarn.appMasterEnv.ENVIRON=PROD" \
    --conf "spark.yarn.appMasterEnv.SRC_DIR=s3://itv-emr-studio/itv-emr-studio/prod/landing/ghactivity/" \
    --conf "spark.yarn.appMasterEnv.SRC_FILE_FORMAT=json" \
    --conf "spark.yarn.appMasterEnv.TGT_DIR=s3://itv-emr-studio/itv-emr-studio/prod/raw/ghactivity/" \
    --conf "spark.yarn.appMasterEnv.TGT_FILE_FORMAT=parquet" \
    --conf "spark.yarn.appMasterEnv.SRC_FILE_PATTERN=2021-01-13" \
    --py-files itv-ghactivity.zip \
    app.py
  ```

**Run Spark Applications using Step Execution**

- in AWS web interface, can add steps for existing clusters or while creating a cluster
- create step
  - spark application
  - cluster mode
  - add *conf* details and py-files as spark-submit options
  - need to have program in S3 and specify path to .py file
  - no need for arguments
  - action on failure *continue* and *cancel and wait* behave similar for just one step
- create step and wait for it to run
- can validate by checking logs, use notebook on cluster, create glue catalog table and use Athena, or run commands against S3 to check if data is there





