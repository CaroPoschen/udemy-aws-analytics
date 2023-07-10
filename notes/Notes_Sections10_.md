# Data Engineering using AWS Analytics Services

**Sections 10 - **



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









