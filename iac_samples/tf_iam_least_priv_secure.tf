provider "aws" { region = "us-east-1" }

variable "bucket_arn" { default = "arn:aws:s3:::jj-demo-private-bucket-001" }

data "aws_iam_policy_document" "s3_readonly" {
  statement {
    effect = "Allow"
    actions = ["s3:GetObject", "s3:ListBucket"]
    resources = [
      var.bucket_arn,
      "${var.bucket_arn}/*"
    ]
  }
}

resource "aws_iam_policy" "s3_readonly" {
  name   = "jjS3ReadOnlyPolicy"
  policy = data.aws_iam_policy_document.s3_readonly.json
}
