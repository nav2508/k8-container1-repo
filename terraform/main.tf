provider "google" {
  project = "k8s-microservices-project"  
  region  = "us-central1"
}

# GKE Cluster Configuration
resource "google_container_cluster" "gke_cluster" {
  name                     = "gke-standard-cluster"
  location                 = "us-central1"
  remove_default_node_pool = true  # Removing default node pool
  initial_node_count       = 1
  enable_autopilot         = false # Standard cluster as required

  network    = "default"
  subnetwork = "default"

  # Enable HTTP Load Balancing (for external access)
  addons_config {
    http_load_balancing {
      disabled = false
    }
  }
}

# Node Pool Configuration
resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-node-pool"
  cluster    = google_container_cluster.gke_cluster.id
  location   = google_container_cluster.gke_cluster.location
  node_count = 1  # Only 1 node to reduce costs

  node_config {
    machine_type = "e2-micro" # 2 vCPUs, 1GB memory
    disk_size_gb = 10
    image_type   = "COS_CONTAINERD" #  Container-Optimized OS

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

#  Persistent Volume (PV) 
resource "kubernetes_persistent_volume" "navya_pv" {
  metadata {
    name = "navya-pv"
  }
  spec {
    capacity = {
      storage = "1Gi"
    }
    access_modes = ["ReadWriteMany"]  #  Multiple pods can access it
    persistent_volume_reclaim_policy = "Retain"
    storage_class_name = "manual"

    persistent_volume_source {
      host_path {
        path = "/Navya_PV_dir"  # Matches your directory structure
      }
    }
  }
}

# Persistent Volume Claim (PVC) 
resource "kubernetes_persistent_volume_claim" "navya_pvc" {
  metadata {
    name = "navya-pvc"
  }
  spec {
    access_modes = ["ReadWriteMany"]  #  Allow multiple pods
    resources {
      requests = {
        storage = "1Gi"
      }
    }
    storage_class_name = "manual"
  }
}

# Output Cluster Information
output "gke_cluster_name" {
  value = google_container_cluster.gke_cluster.name
}

output "gke_cluster_endpoint" {
  value = google_container_cluster.gke_cluster.endpoint
}
