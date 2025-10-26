# Secure: Private RDS, encrypted, IAM auth enabled, backups on
provider "aws" { region = "us-east-1" }

resource "aws_db_instance" "good_rds" {
  identifier                 = "jj-good-rds"
  engine                     = "mysql"
  instance_class             = "db.t3.micro"
  username                   = "admin"
  password                   = "UseSecretManagerOrIAM!"
  allocated_storage          = 20
  publicly_accessible        = false
  storage_encrypted          = true
  backup_retention_period    = 7
  iam_database_authentication_enabled = true
  skip_final_snapshot        = true
}
