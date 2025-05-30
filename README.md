# 🧠 Zabbix Burtforce

> Ethical Brute Force Combo Generator & Login Tester – for educational and authorized penetration testing only.

Goblin Tool is a Python-based utility for generating username-password combinations and testing login forms like Zabbix’s. This tool is strictly for **educational purposes** and **legitimate security assessments** on systems where you have **explicit permission** to test.

## ⚠️ Legal Disclaimer

```
This tool is provided for educational purposes ONLY.

By using Goblin Tool, you agree that:

* You are authorized to perform security testing on the target system.
* You will not use this tool to access systems without permission.
* The author is not responsible for any misuse or damage caused by this software.
````

Using this tool against systems without explicit authorization is **illegal** and against GitHub’s terms of service.

## ✨ Features

- ✅ Generate all possible `username:password` combinations
- ✅ DOM-based brute force tester (tested on Zabbix login)
- ✅ Beautiful output with real-time progress
- ✅ Auto User-Agent rotation to simulate real-world traffic
- ✅ Suspicious login attempt logging

## 🔧 Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/BDadmehr0/zabbix-burtforce.git
cd zabbix-burtforce
pip install -r requirements.txt
````

## 🛠️ Usage

### 🔹 1. Generate Username\:Password Combos

```bash
python zabbix_7.0.0_burtforce.py generate -u usernames.txt -p passwords.txt -o combos.txt
```

**Arguments:**

* `-u` Path to a file containing usernames (one per line)
* `-p` Path to a file containing passwords (one per line)
* `-o` Output file to save combinations (default: `combinations.txt`)


### 🔹 2. Run Brute Force Attack (⚠️ Legal use only!)

```bash
python zabbix_7.0.0_burtforce.py bruteforce -t https://example.com/index.php -c combos.txt -d 1
```

**Arguments:**

* `-t` Target login URL (e.g., Zabbix form)
* `-c` File containing username\:password combinations
* `-d` Delay between requests in seconds (default: 1)

📝 If a login attempt does **not** return a known error message, it is marked as **suspicious** and logged in `suspicious_login_attempts.log`.

## 🧩 Example

```bash
python zabbix_7.0.0_burtforce.py generate -u users.txt -p common_passwords.txt -o combos.txt
python zabbix_7.0.0_burtforce.py bruteforce -t http://localhost/zabbix/index.php -c combos.txt -d 0.5
```

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgements

* Inspired by common tools like THC-Hydra & Burp Suite
* For ethical hackers, pentesters, and students in cybersecurity

## 🔐 Reminder

> ❗ **You are responsible** for all activity using this tool. Always have written authorization before using it on any system.
