output "vpc_id" {
  value       = aws_vpc.main.id
  description = "The ID of the VPC"
}

output "alb_dns_name" {
  value       = aws_lb.main.dns_name
  description = "The public DNS name of the ALB"
}

output "rds_endpoint" {
  value       = aws_db_instance.main.endpoint
  description = "The endpoint of the RDS PostgreSQL instance"
}

output "redis_endpoint" {
  value       = aws_elasticache_cluster.main.cache_nodes[0].address
  description = "The address of the Redis instance"
}
