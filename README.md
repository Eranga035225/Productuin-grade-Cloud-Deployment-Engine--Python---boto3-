# 🚀 Cloud Deployment Engine (Production-Style AWS Automation using Python + boto3)

## 📌 Overview
This project is a **production-style cloud deployment engine** that automates AWS infrastructure provisioning using Python and boto3.  
It replaces manual AWS console operations with a **reproducible, CI/CD-driven workflow**.

---

## 🏗️ Architecture

Client → Application Load Balancer → EC2 → Web Application

- **ALB** handles incoming traffic  
- Routes requests to EC2 instance  
- EC2 is bootstrapped using user data scripts  
- Website deployed automatically  

---

## ⚙️ Features

### 🔹 Infrastructure Automation
- EC2 instance provisioning
- Dynamic Amazon Linux AMI selection
- Automated key pair management
- Security group creation and configuration

### 🔹 Load Balancing
- Application Load Balancer (ALB)
- Target group creation and registration
- Listener configuration for HTTP traffic

### 🔹 Deployment Automation
- User-data based bootstrapping
- Zero manual server configuration
- Automatic website deployment

### 🔹 Lifecycle Management
- Tag-based resource identification
- Safe and controlled cleanup (destroy)
- Dependency-aware teardown: