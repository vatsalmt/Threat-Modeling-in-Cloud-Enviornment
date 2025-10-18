import csv
import json
import os

mapping_file = "../docs/mapping_rules.csv"
manual_threats_file = "../manual_analysis/manaual_result.csv"
scanner_results_file = "../auto_scan_results/checkov_results.json"
output_file = "../auto_scan_results/predicted_threats.csv"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Load mapping rules
mapping_rules = []
with open(mapping_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    mapping_rules = list(reader)

# Load manual threats (optional)
manual_threats = []
if os.path.exists(manual_threats_file):
    with open(manual_threats_file, newline='', encoding='utf-8') as f:
        manual_threats = list(csv.DictReader(f))

# Load Checkov results
with open(scanner_results_file, encoding='utf-8') as f:
    scan_data = json.load(f)

# Collect all checks (passed + failed)
all_findings = []
if isinstance(scan_data, list):
    for entry in scan_data:
        results = entry.get("results", {})
        all_findings.extend(results.get("failed_checks", []))
        all_findings.extend(results.get("passed_checks", []))
else:
    results = scan_data.get("results", {})
    all_findings.extend(results.get("failed_checks", []))
    all_findings.extend(results.get("passed_checks", []))

# Map Checkov finding to STRIDE/ATT&CK
def map_to_threats(check_id, description):
    for rule in mapping_rules:
        if rule["check_id"] == check_id or rule["pattern"].lower() in description.lower():
            return rule["STRIDE"], rule["ATTCK"]
    return "Uncategorized", "-"

mapped_results = []
for finding in all_findings:
    check_id = finding.get("check_id", "")
    resource = finding.get("resource", "")
    description = finding.get("check_name", "")
    severity = finding.get("severity", "N/A")

    stride, attck = map_to_threats(check_id, description)
    mapped_results.append({
        "Resource": resource,
        "Description": description,
        "Check_ID": check_id,
        "STRIDE": stride,
        "ATTCK_ID": attck,
        "Severity": severity,
        "Source": "Automated"
    })

# Merge manual threats
for t in manual_threats:
    t["Source"] = "Manual"
    mapped_results.append(t)

# Debug info
print(f"[+] Total mapped results: {len(mapped_results)}")

# Write output CSV
with open(output_file, "w", newline='', encoding='utf-8') as f:
    fieldnames = ["Resource", "Description", "Check_ID", "STRIDE", "ATTCK_ID", "Severity", "Source"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(mapped_results)

print(f"[+] Mapped results saved to: {output_file}")
