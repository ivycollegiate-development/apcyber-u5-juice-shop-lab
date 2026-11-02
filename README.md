# AP Cyber Unit 5 Lab: OWASP Juice Shop — SQL Injection & XSS

**Course**: AP Computer Science Principles — Cybersecurity
**Unit**: 5 — Application & Data Security
**Topic**: 5.1 Application Vulnerabilities (SQLi, XSS, CSRF)

---

## Lab Overview

In this lab, you will exploit **SQL Injection (SQLi)** and **Cross-Site Scripting (XSS)** vulnerabilities in the OWASP Juice Shop — a deliberately vulnerable web application. You will document your findings and submit them via GitHub Actions for automated grading.

---

## Learning Objectives

By the end of this lab, you will be able to:
- ☐ Identify and exploit **SQL Injection** in login, search, and feedback forms
- ☐ Identify and exploit **Reflected XSS** and **Stored XSS** vectors
- ☐ Document vulnerabilities with evidence (screenshots, requests, responses)
- ☐ Map findings to **OWASP Top 10** and **MITRE ATT&CK** techniques
- ☐ Submit findings via GitHub Actions for automated validation

---

## Prerequisites

- ☐ GitHub account with access to `ivycollegiate-development` organization
- ☐ Codespaces enabled (or Docker locally)
- ☐ Pre-lab worksheet completed (Lesson: Pre-Lab Juice Shop Lab Prep)

---

## Repository Structure

```
apcyber-u5-juice-shop-lab/
├── juice-shop/                 # Juice Shop source (submodule or Docker)
├── attacker_scripts/           # Your exploit scripts
│   ├── sqli_login.py
│   ├── sqli_search.py
│   ├── xss_reflected.py
│   └── xss_stored.py
├── findings_template.csv       # Submit findings here
├── screenshots/                # Evidence screenshots
├── tests/
│   └── test_findings.py        # GitHub Actions validation
├── .github/workflows/
│   └── grade.yml               # Auto-grading workflow
├── docker-compose.yml          # Juice Shop + PostgreSQL
└── README.md                   # This file
```

---

## Quick Start (Codespaces)

1. **Fork this repository** to your GitHub account
2. **Open in Codespaces**: Code → Codespaces → Create codespace on main
3. **Start Juice Shop**:
   ```bash
   docker-compose up -d
   ```
4. **Access Juice Shop**: Ports tab → port 3000 → make Public → open URL
5. **Run exploit scripts** from `attacker_scripts/`
6. **Document findings** in `findings_template.csv`
7. **Commit & push** → GitHub Actions grades automatically

---

## Lab Procedure

### Phase 1: Reconnaissance (10 min)

- ☐ Explore Juice Shop UI: Register, Login, Search, Feedback, Score Board
- ☐ Identify input fields: login form, search bar, feedback form, product reviews
- ☐ Check **Score Board** for challenge hints (shows available vulnerabilities)

### Phase 2: SQL Injection Exploitation (20 min)

#### 2.1 Login Bypass (Authentication Bypass)
- **Target**: `/rest/user/login` endpoint
- **Payload**: `' OR '1'='1' --`
- **Script**: `python3 attacker_scripts/sqli_login.py`
- **Expected**: Login as first user (usually admin) without password

#### 2.2 Search Union Injection
- **Target**: `/rest/products/search?q=` endpoint
- **Payload**: `' UNION SELECT id, email, password, '1', '2', '3', '4', '5', '6', '7' FROM Users--`
- **Script**: `python3 attacker_scripts/sqli_search.py`
- **Expected**: Exfiltrate user credentials from database

### Phase 3: Cross-Site Scripting Exploitation (15 min)

#### 3.1 Reflected XSS
- **Target**: Search results page (`/search?q=`)
- **Payload**: `<script>alert('XSS')</script>`
- **Script**: `python3 attacker_scripts/xss_reflected.py`
- **Expected**: Alert executes in victim's browser when they click crafted link

#### 3.2 Stored XSS (Product Review)
- **Target**: Product review submission (`/api/Reviews/`)
- **Payload**: `<img src=x onerror=alert('Stored XSS')>`
- **Script**: `python3 attacker_scripts/xss_stored.py`
- **Expected**: Script executes when any user views the product page

### Phase 4: Documentation & Submission (5 min)

- ☐ Complete `findings_template.csv` with all 4 findings
- ☐ Add screenshots to `screenshots/` folder
- ☐ Commit and push:
  ```bash
  git add findings_template.csv screenshots/
  git commit -m "Complete Juice Shop findings"
  git push origin main
  ```
- ☐ Check **Actions** tab for grading results

---

## Findings Template (findings_template.csv)

```csv
finding_id,vulnerability_type,owasp_category,mitre_technique,endpoint,payload,evidence,impact,remediation,severity
JUICE-001,SQL Injection,A03:2021-Injection,T1190,/rest/user/login,"' OR '1'='1' --","Screenshot: admin login without password","Authentication bypass → account takeover","Parameterized queries; input validation",High
JUICE-002,SQL Injection,A03:2021-Injection,T1190,/rest/products/search,"' UNION SELECT id,email,password...--","Screenshot: user credentials in search results","Data exfiltration → credential theft","Parameterized queries; least privilege DB user",Critical
JUICE-003,Cross-Site Scripting (Reflected),A03:2021-Injection,T1059.007,/search?q=,<script>alert('XSS')</script>,"Screenshot: alert on search page","Session hijacking, defacement","Output encoding; CSP; input validation",Medium
JUICE-004,Cross-Site Scripting (Stored),A03:2021-Injection,T1059.007,/api/Reviews/,<img src=x onerror=alert('Stored XSS')>,"Screenshot: alert on product page","Persistent attack on all visitors","Output encoding; CSP; sanitize stored input",High
```

---

## Grading Rubric (GitHub Actions)

| Criterion | Points |
|-----------|--------|
| Finding 1: SQLi Login Bypass | 25 pts |
| Finding 2: SQLi Search Union | 25 pts |
| Finding 3: Reflected XSS | 25 pts |
| Finding 4: Stored XSS | 25 pts |
| **Total** | **100 pts** |

**Validation checks**:
- CSV has exactly 4 rows (header + 4 findings)
- All required columns populated
- `finding_id` matches expected: JUICE-001 through JUICE-004
- `vulnerability_type` in {SQL Injection, Cross-Site Scripting (Reflected), Cross-Site Scripting (Stored)}
- `severity` in {Critical, High, Medium, Low}
- Screenshots exist for each finding

---

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Juice Shop won't start | `docker-compose logs` → check PostgreSQL ready; increase `restart: unless-stopped` |
| Port 3000 not accessible | Codespaces → Ports → port 3000 → Visibility: Public |
| SQLi payloads blocked | Try variations: `' OR 1=1--`, `' OR '1'='1' #`, `admin'--` |
| XSS not executing | Check Content-Security-Policy header; try event handlers (`onerror`, `onload`) |
| Actions workflow fails | Check workflow logs; verify CSV formatting (no extra commas, proper quoting) |

---

## Resources

- **OWASP Juice Shop**: https://github.com/juice-shop/juice-shop
- **OWASP Top 10 2021**: https://owasp.org/Top10/
- **SQL Injection Cheat Sheet**: https://portswigger.net/web-security/sql-injection/cheat-sheet
- **XSS Cheat Sheet**: https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
- **MITRE ATT&CK**: https://attack.mitre.org/ (T1190, T1059.007)

---

## Academic Integrity

- ☐ **No sharing flags or payloads** — each student solves independently
- ☐ **Writeups in your own words** — cite any references
- ☐ **Scope**: Only this Juice Shop instance; no external targeting
- ☐ **Violations** → zero for lab + disciplinary referral