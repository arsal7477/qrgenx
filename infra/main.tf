terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "aws" {
  region = var.aws_region
}


module "networking" {
  source      = "./modules/networking"
  app_name    = var.app_name
  environment = var.environment
  aws_region  = var.aws_region
}

module "compute" {
  source        = "./modules/compute"
  app_name      = var.app_name
  environment   = var.environment
  vpc_id        = module.networking.vpc_id
  public_subnets = module.networking.public_subnets
  instance_type = var.instance_type
  key_name      = var.key_name
}

module "monitoring" {
  source = "./modules/monitoring"
  app_name = var.app_name
  environment = var.environment
  vpc_id = module.networking.vpc_id
}
