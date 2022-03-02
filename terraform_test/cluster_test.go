package test

import (
	"os"
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform"
)


func TestTerraformModules(t *testing.T) {
	// retryable errors in terraform testing.
	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../terraform",
		Vars: map[string]interface{}{
			"region": os.Getenv("AWS_REGION"),
			"mongodbatlas_private_key": os.Getenv("MONGODB_ATLAS_PRIVATE_KEY"),
			"mongodbatlas_public_key": os.Getenv("MONGODB_ATLAS_PUBLIC_KEY"),
			"project_id": os.Getenv("MONGODB_ATLAS_PROJECT_ID"),
			"cluster_name": os.Getenv("MONGODB_ATLAS_CLUSTER_NAME"),
			"cluster_size": os.Getenv("MONGODB_ATLAS_CLUSTER_SIZE"),
			"database_name": os.Getenv("DATABASE_NAME"),
			"db_username": os.Getenv("DB_USERNAME"),
			"db_password": os.Getenv("DB_PASSWORD"),
		},
	})

	defer terraform.Destroy(t, terraformOptions)

	terraform.InitAndApply(t, terraformOptions)

}
