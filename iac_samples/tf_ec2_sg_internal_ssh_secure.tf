provider "aws" { region = "us-east-1" }

variable "office_cidr" { default = "10.0.0.0/24" }

resource "aws_security_group" "ssh_restricted" {
  name        = "ssh-restricted"
  description = "Allows SSH only from office CIDR"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.office_cidr]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
