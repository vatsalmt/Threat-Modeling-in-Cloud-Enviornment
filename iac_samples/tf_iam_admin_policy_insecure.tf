provider "aws" { region = "us-east-1" }

data "aws_iam_policy_document" "admin" {
  statement {
    effect = "Allow"
    actions   = ["*"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "admin" {
  name   = "jjAdminAll"
  policy = data.aws_iam_policy_document.admin.json
}
