# aws-lambda-s3-trigger

This project uses a combination of serverless and terraform to create a lambda that is trigged when
a csv (can be customized in `serverless.yml` file) is created in s3.


After trigged the python code creates a stream with limitation (chunck size) to read each line and
obtain a structured data to easy access.


The serverless is configured to encrypted all s3 files using AWS KMS even as Lambda function.


Continuos integrations has developed using Github actions. More detalis in `.github/worflows` folder.

# Data processing

The sample utilized for this project is `example/municipalities.csv`. This file contains all municipalities 
of Brazil.


## Usage for other csv

Must be contains headers and csv delimiter is `;` that can easyly configurated in `fieldDelimiter`. 


## Data access

You can change `row.get('HEADER')` to get a value

## Limitations

The max chunck size is limited to 1MB (s3 select limitation)

## Terraform Cloud

Used to manage terraform state. https://app.terraform.io/

### Variables

After create your terraform cloud account and started new workspace. Same variables must be created to apply changes


`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. Both generated in AWS IAM with programmatically access mode

## Github Actions


### Secrets

`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. See more information above.


`TF_API_TOKEN` generated in terraform cloud. `Settings > Tokens > Create an API token`


## Features

- S3
- Lambda
- Provider
- KMS
- Python 3.8
