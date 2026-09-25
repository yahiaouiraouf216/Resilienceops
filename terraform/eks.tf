resource "aws_eks_cluster" "resilienceops" {
  name     = "resilienceops"
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids = [
      aws_subnet.public_a.id,
      aws_subnet.public_b.id
    ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy
  ]

}

resource "aws_eks_node_group" "resilienceops_nodes" {
  cluster_name    = aws_eks_cluster.resilienceops.name
  node_group_name = "resilienceops-nodes"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  instance_types  = ["t3.small"]
  subnet_ids = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id
  ]

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.eks_ecr_policy
  ]
}