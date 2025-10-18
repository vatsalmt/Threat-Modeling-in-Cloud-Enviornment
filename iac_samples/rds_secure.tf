resource "aws_db_instance" "secure_db" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t3.micro"
  name                 = "mydb"
  username             = var.db_user
  password             = var.db_password

  publicly_accessible  = false        # ✅ Private DB
  skip_final_snapshot  = false        # ✅ Keep final snapshot on delete
  storage_encrypted    = true         # ✅ Encrypted at rest

  vpc_security_group_ids = [aws_security_group.db_sg.id]
}

resource "aws_security_group" "db_sg" {
  name        = "db-secure-sg"
  description = "Allow MySQL access from internal app subnet"

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # ✅ Example: allow internal apps
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

variable "db_user" {
  type      = string
  sensitive = true
}

variable "db_password" {
  type      = string
  sensitive = true
}
