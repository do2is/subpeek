#!/usr/bin/env python3

import __main__
import requests
import time

BANNER = """
    ░██████╗██╗░░██╗██████╗░███████╗███████╗██╗░░░██╗██╗░░██╗
    ██╔════╝██║░░██║██╔══██╗██╔════╝██╔════╝██║░░░██║██║░░██║
    ╚█████╗░███████║██████╔╝█████╗░░█████╗░░╚██╗░██╔╝███████║
    ░╚═══██╗██╔══██║██╔═══╝░██╔══╝░░██╔══╝░░░╚████╔╝░██╔══██║
    ██████╔╝██║░░██║██║░░░░░███████╗███████╗░░╚██╔╝░░██║░░██║
    ╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚══════╝░░░╚═╝░░░╚═╝░░╚═╝
                    ~ Simple Subdomain Peek (HTTPS supported) ~
"""

def load_wordlist(path):
    try:
        with open(path, 'r') as f:
            words = f.read().splitlines()
        return words
    except Exception as e:
        print(f"[!] Failed to load wordlist: {e}")
        return []

def check_subdomain(domain, sub):
    urls = [
        f"https://{sub}.{domain}",
        f"http://{sub}.{domain}"
    ]
    for url in urls:
        try:
            r = requests.get(url, timeout=3)
            if r.status_code < 400:
                return True, r.status_code, url
        except requests.exceptions.RequestException:
            continue
    return False, None, None

def main():
    print(BANNER)
    domain = input("[?] Target domain (e.g. example.com): ").strip()
    wordlist_path = input("[?] Path to wordlist file: ").strip()

    subdomains = load_wordlist(wordlist_path)
    if not subdomains:
        print("[-] No subdomains to scan.")
        return

    print(f"\n[+] Starting scan on {domain} using {len(subdomains)} entries...\n")

    for sub in subdomains:
        live, code, url = check_subdomain(domain, sub)
        if live:
            print(f"[+] Found: {url}  (Status {code})")
        time.sleep(0.2)  # Sleep to look more human

    print("\n[✓] Scan complete.")

if __name__ == "__main__" :
    main()