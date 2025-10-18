# Threat-Modeling-in-Cloud-Enviornment 

🛡️Project Title :
Benchmarking Threat Modeling in Cloud Environments using Infrastructure-as-Code (IaC)
Group 7 — Cyber Forensics

📘 An overview

This project adds useful benchmarks for threat modeling efficacy to the paper "Threat Modeling in Cloud Computing: A Literature Review."

The original study examined current approaches, but it lacked a quantitative assessment.
In order to close that gap, our project uses small Infrastructure-as-Code (IaC) samples (Terraform & AWS CloudFormation) to compare manual vs. semi-automated threat modeling approaches.

We assess two primary factors:

🎯 Accuracy: The precision, recall, and F1-score of automated tools in identifying threats

⏱️ Effort: The amount of time required for each method


⚙️ Methodology (Step by Step)

1️⃣ Gather IaC Samples

We developed several Terraform templates that covered common AWS resources like S3, EC2, and IAM roles; some of them were purposefully insecure, while others were secure.

2️⃣ Define Ground Truth (Manual Threats)

We used STRIDE and MITRE ATT&CK mappings to manually list "true threats" for every IaC file.
This dataset serves as the gold standard.

3️⃣ Automated Scanning

The same IaC files were scanned for configuration errors using Checkov (by Bridgecrew).
The file checkov_results.json contains the scan results.

4️⃣ Map Results to STRIDE + ATT&CK

We developed a mapping file (mapping_rules.csv) that connects ATT&CK techniques (like T1537) and STRIDE categories (like Information Disclosure) to Checkov rule IDs (like CKV_AWS_20).
Checkov output is transformed into standardized threat labels using a Python script called parse_and_map.py.

5️⃣ Benchmarking

We compared:

Manual threats (manual_threats.csv)
Automated threats (predicted_threats.csv)

Metrics used:
1) Precision
2) Recall
3) F1-score
5) Time Taken

This helped us benchmark both accuracy and effort

👩‍💻Authors: 
1) Vatsal Trivedi
2) Parth Kadiya
3) Jenish Patel
