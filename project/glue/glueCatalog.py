import boto3

import os
os.environ.setdefault('AWS_PROFILE', 'itvgithub')

glue_client = boto3.client('glue')
print(glue_client.list_crawlers()['CrawlerNames'])

print(glue_client.get_crawler(
    Name="Retail Crawler"
))

# glue_client.start_crawler(
#     Name="Retail Crawler"
# )

print(glue_client.get_crawler(
    Name="Retail Crawler"
)['Crawler']['State'])

for db in glue_client.get_databases()['DatabaseList']:
    print(db['Name'])

print('\n\n')

for table in glue_client.get_tables(
    DatabaseName='retail_db'
)['TableList']:
    print(table['Name'])

print('\n\n')

print(glue_client.get_table(
    DatabaseName='retail_db',
    Name='orders'
))

print('\n\n')

