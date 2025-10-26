#!/usr/bin/env python3
"""
Cloud Threat Modeling Benchmark — Accuracy Metrics

Reads:
  manual_analysis/manual_analysis.csv
  auto_scan_results/predicted_threats.csv
  auto_scan_results/mapping_rules.csv

Writes (auto-created):
  results/metrics.json
  results/summary.txt
  results/mismatch.csv

Features:
  - Case-insensitive, trimmed comparisons (prevents false errors)
  - Optional minimum-severity filter on predictions (LOW/MEDIUM/HIGH/CRITICAL)
  - Optional requirement to match ATT&CK when present in manual set
  - Clear human-readable summary

Run:
  python accuracy_metrics.py
Optional flags:
  --min-severity medium        (default: low)
  --require-attack-id true     (default: true)

Example:
  python accuracy_metrics.py --min-severity medium --require-attack-id true
"""

import argparse
import json
import os
import sys
import pandas as pd


# -------------------------
# Paths (relative to script)
# -------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
MANUAL_PATH = os.path.join(ROOT, "manual_analysis", "manual_analysis.csv")
PRED_PATH   = os.path.join(ROOT, "auto_scan_results", "predicted_threats.csv")
MAP_PATH    = os.path.join(ROOT, "auto_scan_results", "mapping_rules.csv")
RESULTS_DIR = os.path.join(ROOT, "results")

SEV_ORDER = ["low", "medium", "high", "critical"]


def _norm(s):
    """lowercase + strip; robust to None"""
    if pd.isna(s) or s is None:
        return ""
    return str(s).strip().lower()


def _assert_file(p, label):
    if not os.path.exists(p):
        sys.stderr.write(f"[ERROR] Missing {label} at: {p}\n")
        sys.stderr.write("Tip: Check your folder names and file names.\n")
        sys.exit(1)


def load_inputs():
    _assert_file(MANUAL_PATH, "manual_analysis.csv")
    _assert_file(PRED_PATH, "predicted_threats.csv")
    _assert_file(MAP_PATH, "mapping_rules.csv")

    manual = pd.read_csv(MANUAL_PATH).fillna("")
    pred   = pd.read_csv(PRED_PATH).fillna("")
    mapping= pd.read_csv(MAP_PATH).fillna("")

    # Soft schema checks with helpful messages
    need_manual_cols = {"file","stride","attack_id"}
    if not need_manual_cols.issubset(set(c.lower() for c in manual.columns)):
        sys.stderr.write("[ERROR] manual_analysis.csv must have at least columns: file,stride,attack_id\n")
        sys.exit(1)

    need_pred_cols = {"file","rule_id","severity"}
    if not need_pred_cols.issubset(set(c.lower() for c in pred.columns)):
        sys.stderr.write("[ERROR] predicted_threats.csv must have columns: file,rule_id,severity (notes optional)\n")
        sys.exit(1)

    need_map_cols = {"rule_id","stride","attack_id"}
    if not need_map_cols.issubset(set(c.lower() for c in mapping.columns)):
        sys.stderr.write("[ERROR] mapping_rules.csv must have columns: rule_id,stride,attack_id\n")
        sys.exit(1)

    # Normalize column names (lowercase) to avoid case issues in headers
    manual.columns  = [c.lower() for c in manual.columns]
    pred.columns    = [c.lower() for c in pred.columns]
    mapping.columns = [c.lower() for c in mapping.columns]

    return manual, pred, mapping


def apply_cleaning_and_mapping(manual, pred, mapping, min_severity, require_attack_id):
    # Normalize text/case
    for col in ["file","resource","stride","attack_id","severity","notes"]:
        if col in manual.columns:
            manual[col] = manual[col].apply(_norm)

    for col in ["file","rule_id","severity","notes"]:
        if col in pred.columns:
            pred[col] = pred[col].apply(_norm)

    for col in ["rule_id","stride","attack_id"]:
        if col in mapping.columns:
            mapping[col] = mapping[col].apply(_norm)

    # Filter predictions by minimum severity
    min_sev = _norm(min_severity)
    if min_sev not in SEV_ORDER:
        raise ValueError(f"Unknown min severity '{min_sev}'. Choose from {SEV_ORDER}.")

    def sev_ok(s):
        s = _norm(s)
        idx = SEV_ORDER.index(s) if s in SEV_ORDER else 0
        return idx >= SEV_ORDER.index(min_sev)

    pred = pred[pred["severity"].apply(sev_ok)].copy()

    # Map rule_id -> STRIDE/ATT&CK
    pred = pred.merge(mapping, on="rule_id", how="left", suffixes=("", "_map"))
    pred["stride_mapped"] = pred["stride"].fillna("")      # from mapping
    pred["attack_mapped"] = pred["attack_id"].fillna("")   # from mapping

    # Prepare keys for matching
    manual["key_file"]   = manual["file"]
    manual["key_stride"] = manual["stride"]
    manual["key_attack"] = manual["attack_id"]
    manual["has_attack"] = manual["key_attack"] != ""

    pred["key_file"]     = pred["file"]
    pred["key_stride"]   = pred["stride_mapped"]
    pred["key_attack"]   = pred["attack_mapped"]

    # Build sets for fast TP/FP/FN math
    manual_set = set()
    for _, r in manual.iterrows():
        # If manual has an attack_id, require exact (case-insensitive) match; else compare only on file+stride
        tup = (r["key_file"], r["key_stride"], r["key_attack"] if r["has_attack"] else "")
        manual_set.add(tup)

    pred_set = set()
    for _, r in pred.iterrows():
        tup = (r["key_file"], r["key_stride"], r["key_attack"] if require_attack_id else "")
        pred_set.add(tup)

    return manual_set, pred_set, pred


def compute_and_write_results(manual_set, pred_set):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    TP = len(manual_set & pred_set)
    FP = len(pred_set - manual_set)
    FN = len(manual_set - pred_set)

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
    recall    = TP / (TP + FN) if (TP + FN) > 0 else 0.0
    f1        = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    # Mismatches detail
    mismatches = []
    for f, s, a in (pred_set - manual_set):
        mismatches.append({"type": "FP", "file": f, "stride": s, "attack_id": a})
    for f, s, a in (manual_set - pred_set):
        mismatches.append({"type": "FN", "file": f, "stride": s, "attack_id": a})

    # Save CSV (sorted for readability)
    if mismatches:
        mdf = pd.DataFrame(mismatches, columns=["type","file","stride","attack_id"]).sort_values(["type","file","stride"])
    else:
        mdf = pd.DataFrame(columns=["type","file","stride","attack_id"])

    mismatch_path = os.path.join(RESULTS_DIR, "mismatch.csv")
    mdf.to_csv(mismatch_path, index=False)

    # Save metrics.json
    metrics = {
        "tp": TP,
        "fp": FP,
        "fn": FN,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }
    with open(os.path.join(RESULTS_DIR, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Save a friendly summary.txt
    with open(os.path.join(RESULTS_DIR, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("ACCURACY SUMMARY\n")
        f.write("----------------\n")
        f.write(f"True Positives (TP): {TP}\n")
        f.write(f"False Positives (FP): {FP}\n")
        f.write(f"False Negatives (FN): {FN}\n\n")
        f.write(f"Precision: {metrics['precision']}   -> Of the tool's flags, how many were correct.\n")
        f.write(f"Recall:    {metrics['recall']}      -> Of the real threats, how many the tool caught.\n")
        f.write(f"F1-score:  {metrics['f1']}          -> Balance between precision and recall.\n\n")
        f.write("See 'results/mismatch.csv' for what was extra (FP) or missed (FN).\n")

    return metrics, mismatch_path


def parse_args():
    parser = argparse.ArgumentParser(description="Compute accuracy metrics for cloud threat modeling benchmark.")
    parser.add_argument("--min-severity", default="low",
                        help="Minimum prediction severity to include: low|medium|high|critical (default: low)")
    parser.add_argument("--require-attack-id", default="true",
                        help="true|false. If true, when manual row has an ATT&CK ID, predictions must match it. (default: true)")
    return parser.parse_args()


def main():
    args = parse_args()
    require_attack = str(args.require_attack_id).strip().lower() in ("1","true","yes","y")

    try:
        manual, pred, mapping = load_inputs()
        manual_set, pred_set, _ = apply_cleaning_and_mapping(
            manual, pred, mapping,
            min_severity=args.min_severity,
            require_attack_id=require_attack
        )
        metrics, mismatch_path = compute_and_write_results(manual_set, pred_set)
    except Exception as e:
        sys.stderr.write(f"[ERROR] {e}\n")
        sys.exit(1)

    # Console echo
    print(json.dumps(metrics, indent=2))
    print(f"Wrote mismatches to: {mismatch_path}")
    print("Done.")


if __name__ == "__main__":
    main()
