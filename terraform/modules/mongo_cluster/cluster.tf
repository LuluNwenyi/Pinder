variable "project_id" {}
variable "cluster_name" {}
variable "cluster_size" {}
variable "region" {}

resource "mongodbatlas_cluster" "cluster" {
  project_id   = var.project_id   // Your mongodb atlas project id
  name         = var.cluster_name // Desired cluster name
  disk_size_gb = 2                // Desired disk size in GB

  mongo_db_major_version = "4.2"

  //Provider Settings "block"
  provider_name               = "TENANT"
  backing_provider_name       = "AWS"
  provider_instance_size_name = var.cluster_size // Could be anything above M2. M0 is not supported via this provider
  provider_region_name        = var.region       // Desired region
}
