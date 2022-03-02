

output "mongodb_uri" {
  value       = mongodbatlas_cluster.cluster.connection_strings[0].standard
  description = "MongoDB Atlas URI"
}
