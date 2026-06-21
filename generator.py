import time
import random
from datetime import datetime

# Configuration
LOG_FILE = "auth.log"
TARGET_IP = "192.168.1.50"
ATTACKER_IP = "203.0.113.5"
NORMAL_IPS = ["192.168.1.10", "192.168.1.12", "10.0.0.4"]
USERS = ["admin", "root", "user1", "ssh_user", "guest"]

def generate_logs():
    print(f"[*] Generating simulated logs in '{LOG_FILE}'...")
    
    with open(LOG_FILE, "w") as f:
        # 1. Simulate normal user traffic (Successful logins & occasional typos)
        for _ in range(30):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip = random.choice(NORMAL_IPS)
            user = random.choice(USERS[2:]) # normal users
            status = "Accepted" if random.random() > 0.1 else "Failed"
            f.write(f"{timestamp} src_ip={ip} dest_ip={TARGET_IP} user={user} status={status} message=SSH login attempt\n")
            
        # 2. Simulate a Brute Force Attack (True Positive)
        print("[*] Injecting Brute Force Attack scenario...")
        for _ in range(15):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Rapid failed attempts from the attacker IP
            f.write(f"{timestamp} src_ip={ATTACKER_IP} dest_ip={TARGET_IP} user=root status=Failed message=SSH login attempt\n")
            
        # Attacker finally succeeds
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} src_ip={ATTACKER_IP} dest_ip={TARGET_IP} user=root status=Accepted message=SSH login attempt\n")

        # 3. Simulate a False Positive (An admin who forgot their password)
        print("[*] Injecting False Positive scenario...")
        admin_ip = "192.168.1.99"
        for _ in range(4): # Enough to trigger a mild threshold but benign
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} src_ip={admin_ip} dest_ip={TARGET_IP} user=admin status=Failed message=SSH login attempt\n")

    print("[+] Logs generated successfully!")

if __name__ == "__main__":
    generate_logs()