import argparse
import sys
import os

# Ensure the root directory is included in Python's search path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

# Import operational engines
from modules.scanning.port_scanner import run_port_scan
from modules.vulnerabilities.dir_brute import run_dir_brute
from modules.reporting.report import save_scan_report

def display_banner():
    print("""
=====================================================
    💥 PENETRATION TESTING TOOLKIT v1.0 💥
    Developed for Authorized Security Auditing
=====================================================
    """)

def main():
    display_banner()
    
    parser = argparse.ArgumentParser(description="Modular Penetration Testing Framework")
    parser.add_argument("-t", "--target", required=True, help="Target host domain, IP, or URL")
    parser.add_argument("-m", "--module", required=True, choices=["port", "brute", "all"], help="Select scan module")
    parser.add_argument("-p", "--ports", default="common", choices=["common", "all"], help="Port range selection")
    
    args = parser.parse_args()
    target = args.target

    open_ports_results = None
    dir_brute_results = None

    # ---- 1. PORT SCANNER MODULE ----
    if args.module == "port" or args.module == "all":
        try:
            # We explicitly build the list by appending to prevent syntax filter bugs
            ports_list = []
            if args.ports == "common":
                ports_list.append(21)   # FTP
                ports_list.append(22)   # SSH
                ports_list.append(23)   # Telnet
                ports_list.append(25)   # SMTP
                ports_list.append(53)   # DNS
                ports_list.append(80)   # HTTP
                ports_list.append(110)  # POP3
                ports_list.append(443)  # HTTPS
                ports_list.append(3306) # MySQL
                ports_list.append(8080) # HTTP Alternate
            else:
                ports_list = list(range(1, 1025))
                
            open_ports_results = run_port_scan(target, ports_list)
            print(f"\n[*] Port Scan Complete. Found {len(open_ports_results)} open port(s).")
        except Exception as e:
            print(f"\n[!] Port Scanner encountered an error: {e}")
    
    # ---- 2. DIRECTORY BUSTER MODULE ----
    if args.module == "brute" or args.module == "all":
        try:
            web_target = target if target.startswith(('http://', 'https://')) else f"http://{target}"
            dir_brute_results = run_dir_brute(web_target)
            print(f"\n[*] Directory Busting Complete. Found {len(dir_brute_results)} valid path(s).")
        except Exception as e:
            print(f"\n[!] Directory Buster encountered an error: {e}")

    # ---- 3. AUTOMATED REPORT GENERATION ----
    print("\n[*] Compiling assessment brief...")
    try:
        report_path = save_scan_report(target, open_ports=open_ports_results, discovered_paths=dir_brute_results)
        print(f"[+] Success! Complete log compiled at: {report_path}")
    except Exception as e:
        print(f"[!] Reporting Engine failed to write file: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan suite aborted by user execution.")
        sys.exit(0)


