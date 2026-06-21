# Incident Response & Triage Report: SSH Brute Force

**Incident ID:** INC-2026-001  
**Severity:** Critical  
**Date/Time:** June 21, 2026  
**Analyst:** [Your Name]  

---

## 1. Detection & Alert Details
The internal Python-SIEM triggered an alert based on Rule `SSH-BF-01`: **More than 5 failed login attempts from a single source within a single log cycle.**

* **Target Asset:** `192.168.1.50` (Internal Server)
* **Triggered Source IP:** `203.0.113.5` (External/Unknown Malicious IP)
* **Total Failed Attempts:** 15
* **Compromise Indicator:** A successful login (`status=Accepted`) was observed for user `root` from the attacking IP immediately following the failed attempts.

---

## 2. Analysis & Classification

### Artifact Review
Upon reviewing `auth.log`, two anomalies were identified:
1.  **IP 203.0.113.5:** Showed rapid-fire automated login attempts targeting the `root` account, concluding with a successful authentication bypass.
2.  **IP 192.168.1.99:** Showed 4 failed login attempts for user `admin`. 

### Classification Matrix
* **Alert 1 (IP 203.0.113.5):** **True Positive (Active Compromise)**. The high frequency of failed attempts combined with a final successful login indicates a successful brute force attack.
* **Alert 2 (IP 192.168.1.99):** **False Positive (Benign Behavior)**. Cross-referencing internal asset sheets confirmed this IP belongs to the Network Administrator. The 4 attempts were human error (typos) and did not breach security thresholds.

---

## 3. Containment & Eradication Steps (Playbook)

To mitigate the active True Positive compromise, the following IR lifecycle steps must be executed:

1.  **Network Isolation:** Immediately apply a firewall rule on the perimeter router/host to drop all traffic from `203.0.113.5`.
2.  **Session Termination:** Terminate all active SSH sessions originating from `203.0.113.5` on the target host (`192.168.1.50`).
3.  **Credential Revocation:** Force an immediate password reset for the `root` account.
4.  **Log Preservation:** Export `auth.log` and system audit logs to a secure forensic server for deeper analysis to check if the attacker established persistence (e.g., adding unauthorized keys to `.ssh/authorized_keys`).

---

## 4. Lessons Learned & Recommendations
* **Disable Root SSH:** Modify `/etc/ssh/sshd_config` to set `PermitRootLogin no`.
* **Implement MFA:** Enforce Multi-Factor Authentication for all SSH access.
* **Rate Limiting:** Deploy `Fail2Ban` to automatically drop IPs after 3 failed login attempts before it hits the SIEM level.