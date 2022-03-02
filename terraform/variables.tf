// declaring variables

variable "project_id" {
  type        = string
  description = "project ID"
  default     = null // project ID
}

variable "cluster_name" {
  type        = string
  description = "Cluster name"
  default     = null
}

variable "cluster_size" {
  type        = string
  description = "Cluster size name"
  default     = null // cluster tier 
}

variable "region" {
  type        = string
  description = "Region name"
  default     = "AF_SOUTH_1" // desired aws region
}

variable "mongodbatlas_private_key" {
  type        = string
  description = "MongoDB Atlas private key"
  default     = null // MongoDB Atlas private key
  //sensitive   = true
}

variable "mongodbatlas_public_key" {
  type        = string
  description = "MongoDB Atlas public key"
  default     = null // MongoDB Atlas public key
  //sensitive   = true
}

variable "db_username" {
  type        = string
  description = "Database user's name"
  default     = null
}

variable "db_password" {
  type        = string
  description = "Database user's password"
  default     = null
}

variable "database_name" {
  type        = string
  description = "App database name"
  default     = null
}
