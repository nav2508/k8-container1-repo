provider "google" {
  project = "k8s-microservices-project"
  region  = "us-central1"
}

# GKE Cluster Configuration
resource "google_container_cluster" "gke_cluster" {
  name                     = "gke-standard-cluster"
  location                 = "us-central1"
  initial_node_count       = 1   
  enable_autopilot         = false  

  network    = "default"
  subnetwork = "default"

  # Enable HTTP Load Balancing (for external access)
  addons_config {
    http_load_balancing {
      disabled = false
    }
  }
}

# Node Pool Configuration (Manual)
resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-node-pool"
  cluster    = google_container_cluster.gke_cluster.id
  location   = google_container_cluster.gke_cluster.location
  node_count = 1  

  node_config {
    machine_type = "e2-micro" 
    disk_size_gb = 10
    image_type   = "COS_CONTAINERD" 

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}


resource "kubernetes_persistent_volume" "navya_pv" {
  metadata {
    name = "navya-pv"
  }
  spec {
    capacity = {
      storage = "1Gi"
    }
    access_modes = ["ReadWriteMany"]
    persistent_volume_reclaim_policy = "Retain"
    storage_class_name = "manual"

    persistent_volume_source {
      host_path {
        path = "/Navya_PV_dir"
      }
    }
  }
}


resource "kubernetes_persistent_volume_claim" "navya_pvc" {
  metadata {
    name = "navya-pvc"
  }
  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = "1Gi"
      }
    }
    storage_class_name = "manual"
  }
}


output "gke_cluster_name" {
  value = google_container_cluster.gke_cluster.name
}

output "gke_cluster_endpoint" {
  value = google_container_cluster.gke_cluster.endpoint
}
