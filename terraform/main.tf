

module "cluster" {
  source       = "./modules/mongo_cluster"
  region       = var.region
  cluster_name = var.cluster_name
  cluster_size = var.cluster_size
  project_id   = var.project_id
}
