resource "aws_ecr_repository" "resilienceops" {
  name                 = "resilienceops"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}