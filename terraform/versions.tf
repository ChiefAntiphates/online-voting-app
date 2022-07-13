terraform {
  required_version  = ">= 1.2.5"
  required_providers {
    aws = {
        source  = "hashicorp/aws"
        version = ">= 4.22.0"
    }
    random = {
        source  = "hashicorp/random"
        version = ">= 3.0"
    }
    cloudinit = {
        source  = "hashicorp/cloudinit"
        version = ">= 2.1"
    }
  }
}