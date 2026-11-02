#!/usr/bin/env python3
"""
Test script for GitHub Actions validation of Juice Shop findings.
Validates findings.csv format and content.
"""
import csv
import sys
import os

EXPECTED_FINDINGS = {
    "JUICE-001": {
        "vulnerability_type": "SQL Injection",
        "owasp_category": "A03:2021-Injection",
        "mitre_technique": "T1190",
        "endpoint": "/rest/user/login",
        "severity": "High"
    },
    "JUICE-002": {
        "vulnerability_type": "SQL Injection",
        "owasp_category": "A03:2021-Injection",
        "mitre_technique": "T1190",
        "endpoint": "/rest/products/search",
        "severity": "Critical"
    },
    "JUICE-003": {
        "vulnerability_type": "Cross-Site Scripting (Reflected)",
        "owasp_category": "A03:2021-Injection",
        "mitre_technique": "T1059.007",
        "endpoint": "/search?q=",
        "severity": "Medium"
    },
    "JUICE-004": {
        "vulnerability_type": "Cross-Site Scripting (Stored)",
        "owasp_category": "A03:2021-Injection",
        "mitre_technique": "T1059.007",
        "endpoint": "/api/Reviews/",
        "severity": "High"
    }
}

REQUIRED_COLUMNS = [
    "finding_id", "vulnerability_type", "owasp_category", "mitre_technique",
    "endpoint", "payload", "evidence", "impact", "remediation", "severity"
]

VALID_VULN_TYPES = {
    "SQL Injection",
    "Cross-Site Scripting (Reflected)",
    "Cross-Site Scripting (Stored)"
}

VALID_SEVERITIES = {"Critical", "High", "Medium", "Low"}

def validate_findings(csv_path):
    errors = []
    warnings = []
    
    if not os.path.exists(csv_path):
        errors.append(f"File not found: {csv_path}")
        return errors, warnings
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Check header
    if reader.fieldnames != REQUIRED_COLUMNS:
        errors.append(f"Invalid columns. Expected: {REQUIRED_COLUMNS}, Got: {reader.fieldnames}")
    
    # Check row count
    if len(rows) != 4:
        errors.append(f"Expected 4 findings, got {len(rows)}")
    
    # Validate each row
    found_ids = set()
    for i, row in enumerate(rows):
        row_num = i + 2  # 1-indexed + header
        finding_id = row.get("finding_id", "").strip()
        
        if not finding_id:
            errors.append(f"Row {row_num}: Missing finding_id")
            continue
        
        if finding_id in found_ids:
            errors.append(f"Row {row_num}: Duplicate finding_id: {finding_id}")
        found_ids.add(finding_id)
        
        # Check expected findings
        if finding_id not in EXPECTED_FINDINGS:
            warnings.append(f"Row {row_num}: Unexpected finding_id: {finding_id}")
        else:
            expected = EXPECTED_FINDINGS[finding_id]
            for field, expected_value in expected.items():
                actual = row.get(field, "").strip()
                if actual != expected_value:
                    errors.append(f"Row {row_num} ({finding_id}): {field} mismatch. Expected '{expected_value}', got '{actual}'")
        
        # Validate vulnerability_type
        vuln_type = row.get("vulnerability_type", "").strip()
        if vuln_type not in VALID_VULN_TYPES:
            errors.append(f"Row {row_num} ({finding_id}): Invalid vulnerability_type: '{vuln_type}'")
        
        # Validate severity
        severity = row.get("severity", "").strip()
        if severity not in VALID_SEVERITIES:
            errors.append(f"Row {row_num} ({finding_id}): Invalid severity: '{severity}'")
        
        # Check all fields populated
        for col in REQUIRED_COLUMNS:
            if not row.get(col, "").strip():
                warnings.append(f"Row {row_num} ({finding_id}): Empty field '{col}'")
    
    # Check all expected findings present
    for exp_id in EXPECTED_FINDINGS:
        if exp_id not in found_ids:
            errors.append(f"Missing expected finding: {exp_id}")
    
    return errors, warnings

if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "findings_template.csv"
    
    print(f"[*] Validating {csv_path}...")
    errors, warnings = validate_findings(csv_path)
    
    if warnings:
        print("\n[WARNINGS]")
        for w in warnings:
            print(f"  ! {w}")
    
    if errors:
        print("\n[ERRORS]")
        for e in errors:
            print(f"  ✗ {e}")
        print(f"\nValidation FAILED: {len(errors)} errors")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All validations passed!")
        sys.exit(0)