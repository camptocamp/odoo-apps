# Local Documentation

## Load csv files from S3

For full data version (integration and production instances) csv data files
can be loaded from S3 bucket.

In your docker-compose.yml file you must specify if it must be done or not
by setting the environment variable `USE_S3` to True of False.

If `USE_S3` is True then you must provide the AWS configuration with the
following environment variables:


    - AWS_ACCES_KEY_ID=xxxxxx
    - AWS_SECRET_ACCESS_KEY=xxxxxx
    - AWS_BUCKETNAME=prod-sf-odoo-data
    - AWS_REGION=eu-central-1


In songs, files that must be downloaded from s3 must be loaded like this:

    load_csv(ctx, 's3://prod-sf-odoo-data/install/user.csv', model)

In case `USE_S3` is false the previous command will be done automatically
to fallback on local file path:

    'data/install/user.csv'
