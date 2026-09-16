# Cloud deployment and costs

For a simple AWS deployment: place a containerized API behind an HTTPS load balancer, use RDS PostgreSQL in private subnets, and send structured application logs to CloudWatch. S3 can hold versioned model artifacts. Security groups should allow database traffic only from the API security group. Cost depends on region, traffic, database size, and free-tier eligibility; use AWS Pricing Calculator before committing. No cloud resources are provisioned by this repository.
