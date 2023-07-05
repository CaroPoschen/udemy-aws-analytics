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



