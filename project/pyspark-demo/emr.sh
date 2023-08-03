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