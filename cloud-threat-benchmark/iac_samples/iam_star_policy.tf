resource "aws_iam_policy" "bad_policy" {
  name   = "admin-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "*",
      Effect = "Allow",
      Resource = "*"
    }]
  })
}
