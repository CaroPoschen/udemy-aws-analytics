# Data Engineering using AWS Analytics Services

**Sections 10 - 16**



## Section 10 - Data Ingestion using Lambda Functions

- default names for lambda function: program *lambda_function*, function *lambda_handler*
- create virtual python environment for project
  Linux: activate as ``source ghad-venv/bin/actiavte``
  Windows: activate as ``ghad-venv\Scripts\activate``
- make a folder for all libraries required for the lambda function and install functions in that
- open pyCharm in the virtual environment and develop lambda function there
- to upload lambda function to AWS Lambda, need to have it zipped
  Linux: ``zip -r ghactivity-downloader.zip lambda-function.py``
  Windows: ``7z a ghactivity-downloader.zip lambda-function.py``
- go to AWS management console, create new Lambda function there, and then upload zip file with function
- to include 3rd party libraries, need to have that in the zip file: first go into the folder with the library, create zip file with all contents from there one level up, then go up and update the zip file with the scripts on the upper level
  Linux:

  ```shell
  rm ghactivity-downloader.zip
  cd ghalib
  zip -r ../ghactivity-downloader.zip .
  cd ..
  zip -g ghactivity-downloader.zip lambda_function.py
  ```

  Windows:

  ```shell
  cd ghalib
  7z a ../ghactivity-downloader.zip .
  cd ..
  7z u ghactivity-downloader.zip lambda_function.py
  ```
  
- write functions to download files from specific location, and upload them to S3, may have to specify the AWS profile

- adjust environment variables in project as necessary

- to upload files to S3 with Lambda, need to have write permissions on S3, can attach role to Lambda function

- have functions to download files and then upload them to S3, valiadte every step incrementally

- probably need to increase storage (and potentially runtime) to execute function

- dataset is added to hourly, want to remember last processed file to continue with the next one, when it is available

  - use bookmarks
  - have file in S3 that only saves the name of the last processed file
  - can then read that and increase name/ time to read the next file and update bookmark

- use AWS EventBridge to schedule the function regularly





## Section 11 - Development Lifecycle for PySpark

- set up virtual environment and install PySpark

  ```shell
  python3 -m venv deod-venv
  .\deod-venv\Scripts\activate
  pip install pyspark
  ```

- open PyCharm in folder above virtual environment and create program to test PySpark

  ```python
  from pyspark.sql import SparkSession
       
  spark = SparkSession. \
      builder. \
      master('local'). \
      appName('GitHub Activity - Getting Started'). \
      getOrCreate()
       
  spark.sql('SELECT current_date').show()
  ```

- write new functions to read, process, and write files

- for productionizing, run it on a multinode cluster with yarn



## Section 12 - Overview of Glue Components

Serverless integration Service

AWS Glue has different components:

- Glue Catalog
  - Glue Crawlers
  - Glue Databases and Tables
- Glue Jobs
- Glue Triggers
- Glue Workflows

Example

- use Glue dataset flights,  crawler *Flights Data Crawler*, database *flights-db*, table *flightscsv*,
  data from S3 bucket: *s3://crawler-public-us-east-1/flight/2016/csv*

- use **Athena** as a serverless query engine to query the data

  - needs S3 bucket to store results

  - select appropriate database or database prefix to run queries

  - check that data is copied successfully:

    ```sql
    SELECT count(1)
    FROM "flights-db".flightscsv;
    ```

  - can save queries and use different workgroups in athena

create **Glue Job** to change file format

- need S3 bucket and role

- bucket: *itv-flights*, policy: *ITVFlightsS3FullPolicy*, role: *ITVFlightsGlueRole*

- create custom policy with these permissions:

  ```json
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "ListObjectsInBucket",
              "Effect": "Allow",
              "Action": [
                  "s3:ListBucket"
              ],
              "Resource": [
                  "arn:aws:s3:::itv-flights"
              ]
          },
          {
              "Sid": "AllObjectActions",
              "Effect": "Allow",
              "Action": "s3:*Object",
              "Resource": [
                  "arn:aws:s3:::itv-flights/*"
              ]
          }
      ]
  }
  ```

- role contains new policy and AWSGlueServiceRole

- need to have role with appropriate permissions to run Glue job
- create job to change data format from csv to parquet
- new visual UI to create jobs instead of way shown in course
- create Glue crawler against new folder in bucket containing parquet files, may need to update IAM role
- run crawler to create the Glue Catalog Table, then run queries in Athena to confirm run

**Trigger**

- create a trigger to run the crawler on demand
- delete flightsparquet folder in S3 to recreate it using the trigger
- start trigger to recreate the folder in S3 and validate using Athena

**Glue Workflow**

- trigger can only trigger one job/ crawler, use a workflow for orchestration
- create workflow by giving it a name, then edit it by adding triggers
- workflow is a simple graph
- create workflow using the two existing crawlers and one job, triggering the first on demand, the others based on the events as the result of the previous step
- drop existing tables and delete S3 bucket before running workflow to be able to validate workflow later
- trigger the workflow and then validate the tables using Athena



## Section 13 - Setup Spark History Server for Glue Jobs

Need Spark History Server to trouble shoot issues related to Spark using Glue Jobs

- when setting up a Glue Job, can choose to save logs in S3 bucket
- can use Spark History Server using AWS CloudFormation or locally on Docker
  ``https://docs.aws.amazon.com/glue/latest/dg/monitor-spark-ui-history.html``

**CLoudFormation**

- stack [template](https://aws-glue-sparkui-prod-us-east-1.s3.amazonaws.com/public/cfn/sparkui.yaml)
- enter parameters for stack and create it, output ``SparkUIPublicUrl`` leads to page with logs
- cheaper to use Docker locally, but need enough local reseources

**Docker**

- clone this [git repository](https://github.com/aws-samples/aws-glue-samples/tree/master)
- folder ``utilities/Spark_UI`` contains docker file and instructions for how to set up the project to use it
- build image and set up parameters, might have to update policies for IAM user



## Section 14 - Deep Dive into Glue Catalog

**Prerequisites for Glue Crawler**

- data in S3 or other supported data stores to crawl meta data to create tables
- highly recommended to have structured data; for data from text files, should have a header
- Glue should have appropriate permissions via IAM role to access the S3 buckets

**Create Catalog Tables**

- upload data to S3 (here JSON)
- create crawler
  - provide name
  - configure IAM Role
  - Configure Source

**Download data and save to S3**

- download data from github archive to analyze, need a lot of data, so use three days worth of data

  ```shell
  mkdir ~/Downloads/ghactivity
  cd ~/Downloads/ghactivity
  wget https://data.gharchive.org/2021-01-13-{0..23}.json.gz
  wget https://data.gharchive.org/2021-01-14-{0..23}.json.gz
  wget https://data.gharchive.org/2021-01-15-{0..23}.json.gz
  ```

- upload data to S3 using web console or AWS CLI into folder *landing/ghactivity*

**Create Glue Catalog Table and Validate using Athena**

- more formal approach is to first create the database and then the crawler in Glue

- create database called *itvghlandingdb*

- create crawler *GHActivity Landing Crawler* to crawl S3 bucket folder and create table and data catalog in Glue, crawler will infer schema from JSON attributes in the data

- when crawler is done, run queries using Athena to validate data

  ```sql
  select count(1) from "ghactivity";
  
  select count(1), count(distinct repo.id) from "ghactivity"
  where type = 'CreateEvent' and payload.ref_type = 'repository';
  
  select substr("created_at", 1, 10), count(1), count(distinct id)
  from "ghactivity"
  where type = 'CreateEvent' and "payload".ref_type = 'repository'
  group by substr("created_at", 1, 10);
  ```

- can use Athena to build dashboards with query results from data in S3 using Glue catalog tables

**Use one Crawler for Multiple Datasets/ Tables**

- use data from retail_db github project from section 6
- create new S3 bucket to store data in there, may need to adjust policy for user
- create crawler, give parent folder for all subfolders, if subfolders are in different folders, need to add all parent folders

**CLI**

- check that current user has CLI access on Glue
  ``aws glue list-crawlers --profile itvgithub --region eu-north-1``
- get details for crawler `` aws glue get-crawler --name "Retail Crawler" --profile itvgithub``
- start crawler `` aws glue start-crawler --name "Retail Crawler" --profile itvgithub``
- confirm status by running previous command `` aws glue get-crawler --name "Retail Crawler" --profile itvgithub``
- now see all created tables in AWS Console or using ``aws glue get-databases --profile itvgithub``
- can validate in Athena again
- can check tables similarly
- crawlers usually created in web console, but can be run using CLI or script, to create/ update the tables

**Managing Glue Catalog using Boto3**

- drop table retail_db
- run commands in python to get status and information on crawlers, tables and databases



## Section 15 - Exploring Glue Job APIs

- need read permission on landing folder and write permission on raw folder, may need to adjust policy
- create new job to transform json files to parquet
- run newly created job
- job failed for missing delete permission on S3 bucket, adjust policy
- delete files that were copied in S3 folder to rerun job completely, then rerun job again
- after successful run, can create new crawler to update Glue catalog to run queries in Athena to verify
- may run into issues because of null values in data when transforming to parquet, will be addressed later

**Use Partition when transforming data**

- change script to this:

  ```python
  import sys
  from awsglue.transforms import *
  from awsglue.utils import getResolvedOptions
  from pyspark.context import SparkContext
  from pyspark.sql.functions import date_format, substring
  from awsglue.context import GlueContext
  from awsglue.job import Job
  from awsglue.dynamicframe import DynamicFrame
   
  ## @params: [JOB_NAME]
  args = getResolvedOptions(sys.argv, ['JOB_NAME'])
   
  sc = SparkContext()
  glueContext = GlueContext(sc)
  spark = glueContext.spark_session
  job = Job(glueContext)
  job.init(args['JOB_NAME'], args)
   
  datasource0 = glueContext. \
    create_dynamic_frame. \
    from_catalog(
      database = "itvghactivitylandingdb",
      table_name = "ghactivity",
      transformation_ctx = "datasource0"
    )
   
  df = datasource0. \
    toDF(). \
    withColumn('year', date_format(substring('created_at', 1, 10), 'yyyy')). \
    withColumn('month', date_format(substring('created_at', 1, 10), 'MM')). \
    withColumn('day', date_format(substring('created_at', 1, 10), 'dd'))
   
  dyf = DynamicFrame.fromDF(dataframe=df, glue_ctx=glueContext, name="dyf")
   
  datasink4 = glueContext. \
    write_dynamic_frame. \
    from_options(frame=dyf,
      connection_type="s3",
      connection_options={"path": "s3://itv-github-bucket-1/raw/ghactivity/",
        "compression": "snappy",
        "partitionKeys": ["year", "month", "day"]},
      format="glueparquet",
      transformation_ctx="datasink4")
   
  job.commit()
  ```

- create columns for year, month and day as data frame and then convert back to dynamic frame

- use partition keys year, month, day when transforming data

- most code is the same as previously apart from the partition

- run job

- see files with the new folder structure based on the partitions

- run crawler again to have partitions also in Glue catalog table, to then run Athena queries to validate

- run queries against both source and target to validate that no data is lost



## Section 16 - Glue Job Bookmarks

In production, want incremental processing: regularly update data, can use Glue bookmarks for that, too remember last processed job

- delete data from raw bucket to update it using incremental processing
- list all Glue jobs in CLI assuming proper credentials are configured: ``aws glue list-jobs``
- enable bookmarking for job in console, then run job again
- after successful run of the job, run Athena queries again for validation

**CLI** assuming proper credentials are configured

- list all jobs: ``aws glue list-jobs``
- get details of specific job: ``aws glue get-job --job-name [job name]``
  - see all information for a job here
  - can also check that bookmarks are enabled under default arguments: *"--job-bookmark-option": "job-bookmark-enable"*
- get details about job runs: ``aws glue get-job-runs --job-name [job name]``, descending order, including error message
- to get information about a specific run: ``aws glue get-job-runs --job-name [job name] --run-id [run id]``, requires AWS CLI v2
- get bookmark information: ``aws glue get-job-bookmark --job-name [job name]``
- reset bookmark: removes the bookmark, so job can start again from the beginning, can also reset to a particular run using run id: ``aws glue reset-job-bookmark --job-name [job name]``

**Use bookmarks for new data**

- download data github activity data for new date: ``wget https://data.gharchive.org/2021-01-16-{0..23}.json.gz``

- upload data to s3

  ```shell
  aws s3 cp . s3://itv-github-bucket-1/landing/ghactivity/ \
  	--exclude "*" \
  	--include "2021-01-16*" \
  	--recursive
  ```

- check that data is on s3: ``aws s3 ls s3://itv-github-bucket-1/landing/ghactivity/``

- list all days for which data is currently in the raw zone (proccessed by the job): ``aws s3 ls s3://itv-github-bucket-1/raw/ghactivity/year=2021/month=01/``

- get bookmark information on job: ``aws glue get-job-bookmark --job-name github-json_to_parquet``

- start job from console, returns run id

  ```shell
  aws glue \
  	start-job-run \
  	--job-name github-json_to_parquet \
  	--worker-type G.1X \
  	--number-of-workers 10
  ```

- get job status: ``aws glue get-job-run --job-name github-json_to_parquet --run-id [run id]``

**Validate job run with bookmark**

- check bookmark info: ``aws glue get-job-bookmark --job-name github-json_to_parquet``

- check new folder for month in S3: ``aws s3 ls s3://itv-github-bucket-1/raw/ghactivity/year=2021/month=01/``

- check all files and their upload date/time in S3: ``aws s3 ls s3://itv-github-bucket-1/raw/ghactivity/year=2021/month=01/ --recursive``, all files for first three days around the same time, new day at a different time

- need to recrawl the bucket to update the glue catalog table

- get information about table:

  ```shell
  aws glue get-table \
  --database-name itvghactivityrawdb \
  --name ghactivity
  ```

- get details about partitions:

  ```shell
  aws glue get-partitions \
  	--database-name itvghactivityrawdb \
  	--table-name ghactivity
  ```

- recrawl the table: ``aws glue start-crawler --name "GHActivity Raw Crawler"``

- check partitions again in CLI and see new partition for newly added data

- Cannot just run query in Athena when using partitions (Schema mismatch)

- need to drop partitions in Athena to run queries, check AWS User Guide

- drop partition (enough to just drop one partition) and then repair table:

  ```sql
  ALTER TABLE itvghactivityrawdb.ghactivity
  DROP PARTITION (year = '2021', month = '01', day = '16');
  
  show partitions itvghactivityrawdb.ghactivity;
  
  msck repair table itvghactivityrawdb.ghactivity;
  
  show partitions itvghactivityrawdb.ghactivity;
  ```

- the run count on table and compare with previous runs to see added data:
  ``select count(1) from itvghactivityrawdb.ghactivity;``





