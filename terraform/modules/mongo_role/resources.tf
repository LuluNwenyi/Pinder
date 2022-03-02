variable "project_id" {}

resource "mongodbatlas_custom_db_role" "owner_role" {
  project_id = var.project_id
  role_name  = dbOwner

  actions {
    action = "UPDATE"
    resources {
      collection_name = ""
      database_name   = var.database_name
    }
  }
  actions {
    action = "INSERT"
    resources {
      collection_name = ""
      database_name   = var.database_name
    }
  }
  actions {
    action = "REMOVE"
    resources {
      collection_name = ""
      database_name   = var.database_name
    }
  }
}
