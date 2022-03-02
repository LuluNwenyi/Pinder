variable "cluster_name" {}
variable "project_id" {}
variable "database_name" {}


resource "mongodbatlas_database_user" "user" {
  username           = var.db_username
  password           = var.db_password
  project_id         = var.project_id
  auth_database_name = "admin"

  roles {
    role_name     = "dbOwner"
    database_name = var.database_name
  }

  labels {
    key   = "role"
    value = "Project Owner"
  }

  scopes {
    name = var.cluster_name
    type = "CLUSTER"
  }

}
