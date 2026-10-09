import argparse
import sys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from modules.scanning.port_scanner import run_port_scan
from modules.vulnerabilities.dir_brute import run_dir_brute

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
    parser.add_argument("-t", "--target", required=True, help="Target host")
    parser.add_argument("-m", "--module", required=True, choices=["port", "brute", "all"], help="Select module")
    parser.add_argument("-p", "--ports", default="common", choices=["common", "all"], help="Port range selection")
    
    args = parser.parse_args()
    target = args.target

    try:
        # ---- PORT SCANNER MODULE ----
        if args.module == "port" or args.module == "all":
            if args.ports == "common":
                # Explicit list layout to prevent filtering bugs
                ports_list = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 1433, 3306, 3389, 8080]
            else:
                ports_list = list(range(1, 1025))
                
            open_ports = run_port_scan(target, ports_list)
            print(f"\n[*] Port Scan Complete. Found {len(open_ports)} open port(s).")
        
        # ---- DIRECTORY BUSTER MODULE ----
        if args.module == "brute" or args.module == "all":
            web_target = target if target.startswith(('http://', 'https://')) else f"http://{target}"
            discovered = run_dir_brute(web_target)
            print(f"\n[*] Directory Busting Complete. Found {len(discovered)} valid path(s).")

    except KeyboardInterrupt:
        print("\n[!] Scan suite aborted by user execution.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Critical framework error: {e}")

if __name__ == "__main__":
    main()

