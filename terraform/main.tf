

module "cluster" {
  source       = "./modules/mongo_cluster"
  region       = var.region
  cluster_name = var.cluster_name
  cluster_size = var.cluster_size
  project_id   = var.project_id
}

module "user" {
  source        = "./modules/mongo_user"
  db_username   = var.db_username
  project_id    = var.project_id
  cluster_name  = var.cluster_name
  db_password   = var.db_password
  database_name = var.database_name
}
