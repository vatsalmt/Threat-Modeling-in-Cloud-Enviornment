provider "aws" { region = "us-east-1" }

resource "aws_s3_bucket" "public_bucket" {
  bucket = "jj-demo-public-bucket-001"
  acl    = "public-read"
}

resource "aws_s3_bucket_public_access_block" "pab" {
  bucket = aws_s3_bucket.public_bucket.id
  block_public_acls   = false
  block_public_policy = false
  ignore_public_acls  = false
  restrict_public_buckets = false
}
