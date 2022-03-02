

output "mongodb_uri" {
  description = "Mongo Atlas URI"
  value       = module.cluster.mongodb_uri
}
