variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "qrgenx"  # Set default value here
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"     # Set default value here
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"  # Free tier eligible
}

variable "key_name" {
  description = "SSH key pair name"
  type        = string
  default     = "qrgenx-dev-key"  # Set default value here
}
