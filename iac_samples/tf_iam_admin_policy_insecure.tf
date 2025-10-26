# Insecure: Wildcard IAM policy (Admin)
# Hints: STRIDE=Elevation of Privilege; ATT&CK=T1078 (Valid Accounts), T1098 (Account Manipulation)
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
