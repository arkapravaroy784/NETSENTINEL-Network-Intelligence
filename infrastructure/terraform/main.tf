terraform { required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } } }
provider "aws" { region = var.region }
variable "region" { type = string default = "us-east-1" }
# Intentionally minimal starting point: supply account-specific VPC, CIDRs, and secrets before apply.
