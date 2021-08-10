# ===========================
# CLUSTER
# ===========================
resource "aws_ecs_cluster" "cluster" {
  name = "${var.app}-${var.env}"
}
