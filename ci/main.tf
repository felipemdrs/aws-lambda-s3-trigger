# Describe terraform server https://app.terraform.io/ to manage created resources remotely
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  cloud {
    organization = "felipemdrs"

    workspaces {
      name = "aws-lambda-s3-trigger"
    }
  }
}

# Setup AWS provider
provider "aws" {
  version = "~> 4.8.0"
  region  = "us-east-1"
}
