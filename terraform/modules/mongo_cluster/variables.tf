//declaring variables for the cluster module

variable "mongodbatlas_private_key" {
  type        = string
  description = "MongoDB Atlas private key"
  default     = null // MongoDB Atlas private key
  sensitive   = true
}

variable "mongodbatlas_public_key" {
  type        = string
  description = "MongoDB Atlas public key"
  default     = null // MongoDB Atlas public key
  sensitive   = true
}
