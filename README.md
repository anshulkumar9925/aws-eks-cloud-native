# AWS EKS Cloud-Native Application

A production-style cloud-native application deployment on AWS using
Terraform, Docker, Kubernetes, Amazon EKS, Amazon ECR, RDS PostgreSQL,
IAM, VPC, and GitHub Actions.

## Project Overview

This project demonstrates how to provision AWS infrastructure using
Infrastructure as Code and deploy containerized applications on
Amazon EKS.

## Architecture

Application flow:

User
↓
Application Load Balancer
↓
Amazon EKS
↓
Frontend / Backend Containers
↓
RDS PostgreSQL

Infrastructure:

AWS VPC
├── Public Subnets
│   └── Application Load Balancer
│
└── Private Subnets
    ├── Amazon EKS
    └── RDS PostgreSQL

## Technologies

- AWS
- Amazon EKS
- Amazon ECR
- Amazon RDS
- VPC
- IAM
- Terraform
- Kubernetes
- Docker
- GitHub Actions
- PostgreSQL

## Project Status

🚧 Currently under development.
