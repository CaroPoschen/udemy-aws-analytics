import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1689005951648 = glueContext.create_dynamic_frame.from_catalog(
    database="flights-db",
    table_name="csv",
    transformation_ctx="AWSGlueDataCatalog_node1689005951648",
)

# Script generated for node Change Schema
ChangeSchema_node1689005966886 = ApplyMapping.apply(
    frame=AWSGlueDataCatalog_node1689005951648,
    mappings=[
        ("year", "long", "year", "long"),
        ("quarter", "long", "quarter", "long"),
        ("month", "long", "month", "long"),
        ("day_of_month", "long", "day_of_month", "long"),
        ("day_of_week", "long", "day_of_week", "long"),
        ("fl_date", "string", "fl_date", "string"),
        ("unique_carrier", "string", "unique_carrier", "string"),
        ("airline_id", "long", "airline_id", "long"),
        ("carrier", "string", "carrier", "string"),
        ("tail_num", "string", "tail_num", "string"),
        ("fl_num", "long", "fl_num", "long"),
        ("origin_airport_id", "long", "origin_airport_id", "long"),
        ("origin_airport_seq_id", "long", "origin_airport_seq_id", "long"),
        ("origin_city_market_id", "long", "origin_city_market_id", "long"),
        ("origin", "string", "origin", "string"),
        ("origin_city_name", "string", "origin_city_name", "string"),
        ("origin_state_abr", "string", "origin_state_abr", "string"),
        ("origin_state_fips", "long", "origin_state_fips", "long"),
        ("origin_state_nm", "string", "origin_state_nm", "string"),
        ("origin_wac", "long", "origin_wac", "long"),
        ("dest_airport_id", "long", "dest_airport_id", "long"),
        ("dest_airport_seq_id", "long", "dest_airport_seq_id", "long"),
        ("dest_city_market_id", "long", "dest_city_market_id", "long"),
        ("dest", "string", "dest", "string"),
        ("dest_city_name", "string", "dest_city_name", "string"),
        ("dest_state_abr", "string", "dest_state_abr", "string"),
        ("dest_state_fips", "long", "dest_state_fips", "long"),
        ("dest_state_nm", "string", "dest_state_nm", "string"),
        ("dest_wac", "long", "dest_wac", "long"),
        ("crs_dep_time", "long", "crs_dep_time", "long"),
        ("dep_time", "long", "dep_time", "long"),
        ("dep_delay", "long", "dep_delay", "long"),
        ("dep_delay_new", "long", "dep_delay_new", "long"),
        ("dep_del15", "long", "dep_del15", "long"),
        ("dep_delay_group", "long", "dep_delay_group", "long"),
        ("dep_time_blk", "string", "dep_time_blk", "string"),
        ("taxi_out", "long", "taxi_out", "long"),
        ("wheels_off", "long", "wheels_off", "long"),
        ("wheels_on", "long", "wheels_on", "long"),
        ("taxi_in", "long", "taxi_in", "long"),
        ("crs_arr_time", "long", "crs_arr_time", "long"),
        ("arr_time", "long", "arr_time", "long"),
        ("arr_delay", "long", "arr_delay", "long"),
        ("arr_delay_new", "long", "arr_delay_new", "long"),
        ("arr_del15", "long", "arr_del15", "long"),
        ("arr_delay_group", "long", "arr_delay_group", "long"),
        ("arr_time_blk", "string", "arr_time_blk", "string"),
        ("cancelled", "long", "cancelled", "long"),
        ("cancellation_code", "string", "cancellation_code", "string"),
        ("diverted", "long", "diverted", "long"),
        ("crs_elapsed_time", "long", "crs_elapsed_time", "long"),
        ("actual_elapsed_time", "long", "actual_elapsed_time", "long"),
        ("air_time", "long", "air_time", "long"),
        ("flights", "long", "flights", "long"),
        ("distance", "long", "distance", "long"),
        ("distance_group", "long", "distance_group", "long"),
        ("carrier_delay", "long", "carrier_delay", "long"),
        ("weather_delay", "long", "weather_delay", "long"),
        ("nas_delay", "long", "nas_delay", "long"),
        ("security_delay", "long", "security_delay", "long"),
        ("late_aircraft_delay", "long", "late_aircraft_delay", "long"),
        ("first_dep_time", "long", "first_dep_time", "long"),
        ("total_add_gtime", "long", "total_add_gtime", "long"),
        ("longest_add_gtime", "long", "longest_add_gtime", "long"),
        ("mon", "string", "mon", "string"),
    ],
    transformation_ctx="ChangeSchema_node1689005966886",
)

# Script generated for node Amazon S3
AmazonS3_node1689006014001 = glueContext.write_dynamic_frame.from_options(
    frame=ChangeSchema_node1689005966886,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://itvflights-bucket/flightsparquet/",
        "partitionKeys": [],
    },
    transformation_ctx="AmazonS3_node1689006014001",
)

job.commit()
