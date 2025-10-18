resource "aws_instance" "bad_instance" {
  ami           = "ami-0c55b159cbfafe1f0"  # Example AMI
  instance_type = "t2.micro"
  associate_public_ip_address = true
}
