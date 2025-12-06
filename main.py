#!/usr/bin/env python3
import os
import sys
from termcolor import cprint  # ✅ Make sure termcolor is installed
from utils.config import ensure_output_dir
from utils.recon import run_subfinder, run_amass, probe_alive, check_takeover
from utils.scan import run_nmap, run_whatweb, run_nuclei, run_ffuf
from utils.report import generate_report

# ===============================
#        AUTOMATED BUG BOUNTY TOOLKIT
#            Owner: Jashu
# ===============================

BANNER = r"""
   ___       _   _           _      _   _                  _  _             
  / _ \ __ _| |_| |__   __ _| |_ __| | | |__   ___  ___   | || |__  _   _  
 | | | / _` | __| '_ \ / _` | __/ _` | | '_ \ / _ \/ __|  | || '_ \| | | | 
 | |_| | (_| | |_| | | | | (_| | || (_| | | | |  __/\__ \ | || | | | |_| | 
  \___/ \__,_|\__|_| |_|\__,_|\__\__,_| |_| |_|\___||___/ |_||_| |_|\__, | 
                                                                     |___/  
                       Automated Bug Bounty Toolkit
                               Owner: VulnHunt Reasearch Team
"""

cprint(BANNER, "cyan")


def main():
    # Get domain from environment variable or argument
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = os.getenv("TARGET")
        if not domain:
            print("[!] No TARGET specified. Please set TARGET environment variable or pass as argument.")
            return

    print(f"[*] Scanning TARGET: {domain}")

    # Ensure output folder exists
    ensure_output_dir(domain)

    try:
        # ================= RECON =================
        subfinder_file = run_subfinder(domain)
        amass_file = run_amass(domain)
        alive_file = probe_alive(subfinder_file)

        # Check subdomain takeover
        check_takeover(alive_file)

        # ================= SCAN =================
        with open(alive_file) as f:
            hosts = [line.strip() for line in f.readlines()]

        for host in hosts:
            run_nmap(host, domain)
            run_whatweb(host, domain)
            run_nuclei(host, domain)
            run_ffuf(host, "wordlist.txt", domain)

        # ================= REPORT =================
        generate_report(domain, make_pdf=True)

        print("[✓] Scan completed!")

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Exiting gracefully...")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Exiting gracefully...")
        sys.exit(0)
