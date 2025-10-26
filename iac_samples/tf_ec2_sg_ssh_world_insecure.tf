# Insecure: Security group allows SSH from anywhere
# Hints: STRIDE=Elevation of Privilege/Tampering; ATT&CK=T1021 (Remote Services)
provider "aws" { region = "us-east-1" }

resource "aws_security_group" "ssh_world" {
  name        = "ssh-world"
  description = "Allows SSH from 0.0.0.0/0"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
