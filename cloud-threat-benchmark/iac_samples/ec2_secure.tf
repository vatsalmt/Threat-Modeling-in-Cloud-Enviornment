resource "aws_instance" "secure_instance" {
  ami                    = "ami-0c55b159cbfafe1f0"  # Still needs to be valid in your region
  instance_type          = "t2.micro"
  associate_public_ip_address = false  # 🚫 No public IP — keep it private

  vpc_security_group_ids = [aws_security_group.secure_sg.id]

  tags = {
    Name = "SecureEC2"
  }
}

resource "aws_security_group" "secure_sg" {
  name        = "secure-sg"
  description = "Allow HTTP from internal subnet only"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # ✅ Example private subnet
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
