# Threat-Modeling-in-Cloud-Enviornment

## Project Title
**Benchmarking Threat Modeling in Cloud Environments using Infrastructure-as-Code (IaC)**  
**Group 7 — Cyber Forensics**

---
Loom video of explaining our work
1. Parth - https://www.loom.com/share/cd24935cf49e4839bae12dae0c108b7d?sid=7053cdfd-9d96-431f-843a-e8658f8b8df1
2. Vatsal - https://www.loom.com/share/d0dec8d65c9c4657bec2ae532b9463fa?sid=746c9871-42a3-489b-ab7c-5a6e1173b24c
3. Jenish - https://www.loom.com/share/c2b3f5a38d8340a09668718b3893c549?sid=8ad5503b-8b07-4860-a3f9-4dfe5cb62c89

## An Overview

This project adds useful benchmarks for threat modeling efficacy to the paper **"Threat Modeling in Cloud Computing: A Literature Review."**

The original study examined current approaches, but it lacked a quantitative assessment.  
In order to close that gap, our project uses small **Infrastructure-as-Code (IaC)** samples (Terraform & AWS CloudFormation) to compare **manual vs. semi-automated threat modeling** approaches.

We assess two primary factors:

- **Accuracy:** The precision, recall, and F1-score of automated tools in identifying threats  
- **Effort:** The amount of time required for each method

---

## Methodology (Step by Step)

### 1. Gather IaC Samples
We developed several **Terraform templates** that covered common AWS resources like S3, EC2, and IAM roles;  
some of them were purposefully insecure, while others were secure.

---

### 2. Define Ground Truth (Manual Threats)
We used **STRIDE** and **MITRE ATT&CK** mappings to manually list "true threats" for every IaC file.  
This dataset serves as the **gold standard**.

---

### 3. Automated Scanning
The same IaC files were scanned for configuration errors using **Checkov** (by Bridgecrew).  
The file **`checkov_results.json`** contains the scan results.

---

### 4. Map Results to STRIDE + ATT&CK
We developed a mapping file (**`mapping_rules.csv`**) that connects **ATT&CK techniques** (like `T1537`) and **STRIDE categories** (like *Information Disclosure*)  
to **Checkov rule IDs** (like `CKV_AWS_20`).  

Checkov output is transformed into standardized threat labels using a Python script called **`parse_and_map.py`**.

---

### 5. Benchmarking
We compared:

- Manual threats (**`manual_threats.csv`**)  
- Automated threats (**`predicted_threats.csv`**)

**Metrics used:**
- Precision  
- Recall  
- F1-score  
- Time Taken  

This helped us benchmark both **accuracy** and **effort**.

---

🧑‍💻Authors:

  1) Vatsal  Trivedi  
  MS Cyber Forensics and Security  
🔗 [GitHub](https://github.com/vatsalmt) • [LinkedIn](https://www.linkedin.com/in/vatsal-trivedi18/)

  2) Parth Kadiya  
  MS Cyber Forensics and Security  
🔗 [GitHub](https://github.com/ParthKadiya) • [LinkedIn](https://www.linkedin.com/in/parthkadiya/)

  3) Jenish Patel  
  MS Applied Cybersecurity and Digital Forensics  
🔗 [GitHub](https://github.com/JenishPatel08) • [LinkedIn](https://www.linkedin.com/in/jenish-patel-91ba32316/)



