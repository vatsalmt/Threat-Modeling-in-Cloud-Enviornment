resource "aws_db_instance" "bad_db" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t3.micro"
  name                 = "mydb"
  username             = "foo"
  password             = "barbaz123"
  publicly_accessible  = true
  skip_final_snapshot  = true
  storage_encrypted    = false
}
