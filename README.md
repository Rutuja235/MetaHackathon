---
title: CloudOps Simulator
emoji: ☁️
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# 🚀 CloudOps Environment v4
This environment is live and ready for AI agent evaluation.

### 🔗 Mentor Access Links
* **[Click here to open Interactive API Docs (Swagger UI)](https://rmadhadik-cloudops-eval-v4.hf.space/docs)**
* **[Click here to view Current Environment State (JSON)](https://rmadhadik-cloudops-eval-v4.hf.space/state)**

---

## 📝 Project Overview
This is an **OpenEnv-compliant** simulation. It allows AI agents to practice multi-step DevOps tasks like provisioning storage and compute resources in a safe, sandboxed environment.

### Action Space
The agent can execute the following commands:
1. `create_bucket`: Provision S3-style storage.
2. `provision_ec2`: Deploy a virtual server instance.
3. `add_policy`: Apply IAM security configurations.
