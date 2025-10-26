# Insecure: Publicly accessible RDS with storage unencrypted
# Hints: STRIDE=Information Disclosure; ATT&CK=T1071 (Exfil), T1041 (Exfiltration Over C2)
provider "aws" { region = "us-east-1" }

resource "aws_db_instance" "bad_rds" {
  identifier                 = "jj-bad-rds"
  engine                     = "mysql"
  instance_class             = "db.t3.micro"
  username                   = "admin"
  password                   = "ChangeMe123!"
  allocated_storage          = 20
  publicly_accessible        = true
  storage_encrypted          = false
  skip_final_snapshot        = true
}
