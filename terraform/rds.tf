resource "aws_db_subnet_group" "main" {
  name       = "footprintiq-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "footprintiq-db-subnet-group"
  }
}

resource "aws_security_group" "rds" {
  name        = "footprintiq-rds-sg"
  description = "Allow inbound database traffic from ECS tasks"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "random_password" "db_password" {
  length  = 16
  special = false
}

resource "aws_db_instance" "main" {
  identifier     = "footprintiq-db"
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = var.db_instance_class

  allocated_storage     = 100
  max_allocated_storage = 500
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = "footprintiq"
  username = "footprintiq_admin"
  password = random_password.db_password.result

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 30
  backup_window           = "03:00-04:00"
  maintenance_window      = "mon:04:00-mon:05:00"

  multi_az            = true
  deletion_protection = false # Set to false for dev/tests teardown, true in real prod
  skip_final_snapshot = true

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = {
    Name = "footprintiq-db"
  }
}
