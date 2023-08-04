spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --conf "spark.yarn.appMasterEnv.ENVIRON=PROD" \
  --conf "spark.yarn.appMasterEnv.SRC_DIR=s3://itv-emr-studio/itv-emr-studio/prod/landing/ghactivity/" \
  --conf "spark.yarn.appMasterEnv.SRC_FILE_FORMAT=json" \
  --conf "spark.yarn.appMasterEnv.TGT_DIR=s3://itv-emr-studio/itv-emr-studio/prod/raw/ghactivity/" \
  --conf "spark.yarn.appMasterEnv.TGT_FILE_FORMAT=parquet" \
  --conf "spark.yarn.appMasterEnv.SRC_FILE_PATTERN=2021-01-14" \
  --py-files itv-ghactivity.zip \
  app.py

  --conf "spark.yarn.appMasterEnv.ENVIRON=PROD" --conf "spark.yarn.appMasterEnv.SRC_DIR=s3://itv-emr-studio/itv-emr-studio/prod/landing/ghactivity/" --conf "spark.yarn.appMasterEnv.SRC_FILE_FORMAT=json" --conf "spark.yarn.appMasterEnv.TGT_DIR=s3://itv-emr-studio/itv-emr-studio/prod/raw/ghactivity/" --conf "spark.yarn.appMasterEnv.TGT_FILE_FORMAT=parquet" --conf "spark.yarn.appMasterEnv.SRC_FILE_PATTERN=2021-01-14" --py-files s3://itv-emr-studio/spark-application/app/itv-ghactivity.zip