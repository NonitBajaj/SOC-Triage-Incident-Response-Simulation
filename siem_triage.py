import os
from collections import defaultdict

LOG_FILE = "auth.log"
FAILED_THRESHOLD = 5

def triage_logs():
    if not os.path.exists(LOG_FILE):
        print(f"[-] Error: {LOG_FILE} not found. Run generator.py first.")
        return

    print(f"[*] Parsing {LOG_FILE} for suspicious activity...")
    
    # Track failed attempts per IP
    failed_attempts = defaultdict(int)
    ip_details = defaultdict(list)

    with open(LOG_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(" ")
            # Basic parsing of key-value pairs
            log_data = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=")
                    log_data[k] = v
            
            if log_data.get("status") == "Failed":
                src_ip = log_data.get("src_ip")
                failed_attempts[src_ip] += 1
                ip_details[src_ip].append(log_data)
            elif log_data.get("status") == "Accepted":
                # Track if they eventually succeeded
                src_ip = log_data.get("src_ip")
                ip_details[src_ip].append(log_data)

    # Trigger Alerts based on threshold
    print("\n" + "="*50)
    print(" >>> SIEM ALERT DASHBOARD <<< ")
    print("="*50)
    
    alerts_triggered = 0
    for ip, count in failed_attempts.items():
        if count >= FAILED_THRESHOLD:
            alerts_triggered += 1
            print(f"\n[ALERT #{alerts_triggered}] Brute Force Threshold Exceeded!")
            print(f"  Source IP: {ip}")
            print(f"  Failed Attempts: {count}")
            
            # Check if there was a subsequent successful login
            has_succeeded = any(log.get("status") == "Accepted" for log in ip_details[ip])
            if has_succeeded:
                print("  CRITICAL NOTE: A successful login was detected from this IP after/during the failures!")
            else:
                print("  NOTE: All attempts from this IP failed.")
                
    if alerts_triggered == 0:
        print("[+] No alerts triggered. Environment looks clean.")
    print("\n" + "="*50)

if __name__ == "__main__":
    triage_logs()