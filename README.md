# Threat Modeling in Cloud Environments  
### Benchmarking Manual vs. Semi-Automated Threat Modeling using Infrastructure-as-Code (IaC)

---

## Project Information
**Course:** Cyber Forensics & Security  
**Project Title:** *Benchmarking Threat Modeling in Cloud Environments using Infrastructure-as-Code (IaC)*  
**Group:** 7 — Cyber Forensics

---

## Loom Presentation Videos
| Member | Loom Link |
|:-------|:-----------|
| **Parth** | [Watch Here](https://www.loom.com/share/cd24935cf49e4839bae12dae0c108b7d?sid=7053cdfd-9d96-431f-843a-e8658f8b8df1) |
| **Vatsal** | [Watch Here](https://www.loom.com/share/d0dec8d65c9c4657bec2ae532b9463fa?sid=746c9871-42a3-489b-ab7c-5a6e1173b24c) |
| **Jenish** | [Watch Here](https://www.loom.com/share/c2b3f5a38d8340a09668718b3893c549?sid=8ad5503b-8b07-4860-a3f9-4dfe5cb62c89) |

---

## Overview

This project extends the paper **“Threat Modeling in Cloud Computing: A Literature Review”** by introducing **quantitative benchmarks** for measuring the accuracy and practicality of threat modeling in cloud environments.

Most existing research focuses on qualitative frameworks.  
To close this gap, our work evaluates **how accurate and efficient semi-automated threat modeling tools are** compared to **manual human-led analysis**, using small **Infrastructure-as-Code (IaC)** samples.

---

## Objectives
We assess two primary factors:

- **Accuracy:** Measured using Precision, Recall, and F1-score of Checkov’s detections  
- **Effort:** Measured by comparing time taken for manual vs. automated analysis  

---

## Methodology — Step by Step

### **1️⃣ Gather IaC Samples**
- We have created 10 small Terraform and CloudFormation templates simulating common AWS services like **S3, EC2, IAM, and RDS**.  
- Each file represents either a **secure** or **insecure** configuration.

---

### **2️⃣ Manual Threat Analysis (Ground Truth)**
- We did a manual threat assessment for each  file and mapped it to **STRIDE** and **MITRE ATT&CK** categories.  
- These manual threat assessments are what made up our gold standard dataset and is captured in [`manual_analysis.csv`](manual_analysis/manual_analysis.csv).

---

### **3️⃣ Automated Scanning with Checkov**
- The same IaC files were scanned using **Checkov** (by Bridgecrew).  
- Output was exported as JSON format (`checkov_raw_output.json`) and then converted into CSV (`predicted_threats.csv`).

---

### **4️⃣ Mapping Rules**
- A mapping file [`mapping_rules.csv`](auto_scan_results/mapping_rules.csv) connects:
  - **Checkov rule IDs** → (e.g., `CKV_AWS_20`)  
  - **STRIDE Categories** → (e.g., *Information Disclosure*)  
  - **MITRE ATT&CK IDs** → (e.g., `T1537`)

This ensures consistency between automated and manual results.

---

### **5️⃣ Benchmarking Accuracy**
We compared:
- Manual findings → `manual_analysis.csv`  
- Automated findings → `predicted_threats.csv`

**Metrics Used:**
| Metric | Formula | Meaning |
|:--------|:---------|:--------|
| **Precision** | TP / (TP + FP) | How many detected threats were correct |
| **Recall** | TP / (TP + FN) | How many true threats were detected |
| **F1-score** | 2 × (Precision × Recall) / (Precision + Recall) | Overall balance between accuracy and completeness |

---

### **6️⃣ Efficiency Measurement**
| Method | Duration | Description |
|:--------|:----------|:------------|
| **Manual Analysis** | ~90 minutes | Human inspection of all 10 IaC files |
| **Checkov Scan** | ~6 seconds | Fully automated detection |

Automation offered a **drastic reduction in time**, but manual review revealed more nuanced contextual threats.

---

## Results Summary

| Metric | Value | Interpretation |
|:-------|:------:|:--------------|
| **True Positives (TP)** | 5 | Detected threats correctly matched manual findings |
| **False Positives (FP)** | 0 | No incorrect detections |
| **False Negatives (FN)** | 4 | Missed context-based or subtle threats |
| **Precision** | 1.00 | Perfect detection accuracy |
| **Recall** | 0.56 | Detected ~56 % of real threats |
| **F1-score** | 0.71 | Balanced but incomplete performance |

**Interpretation:**  
Checkov is **accurate** but **not exhaustive** — it identifies major misconfigurations quickly but misses contextual, behavioral, or multi-dimensional threats that require human expertise.

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



