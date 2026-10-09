import argparse
import sys
import os

# Dynamically add the current directory to Python's search path to prevent import errors
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the multi-threaded port scanner module
try:
    from modules.scanning.port_scanner import run_port_scan
except ModuleNotFoundError:
    print("\n[!] Error: Framework cannot locate your modules folder.")
    print("Please ensure your folder structure is: modules/scanning/port_scanner.py")
    sys.path.exit(1)

def display_banner():
    print("""
=====================================================
    💥 PENETRATION TESTING TOOLKIT v1.0 💥
    Developed for Authorized Security Auditing
=====================================================
    """)

def main():
    display_banner()
    
    # 1. Setup terminal arguments
    parser = argparse.ArgumentParser(description="Modular Penetration Testing Framework")
    parser.add_argument("-t", "--target", required=True, help="Target host IP or Domain (e.g., 127.0.0.1 or scanme.nmap.org)")
    parser.add_argument("-p", "--ports", default="common", choices=["common", "all"], 
                        help="Port range to scan. 'common' scans top ports, 'all' scans 1-1024")
    
    args = parser.parse_args()
    target = args.target

    # 2. Determine target ports based on user input
    if args.ports == "common":
        # Standard web, mail, database, and administration ports
        ports_list = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 1433, 3306, 3389, 8080]
    else:
        ports_list = list(range(1, 1025))

    print(f"[*] Initializing suite against target: {target}")
    
    # 3. Fire up the port scanner module
    try:
        open_ports = run_port_scan(target, ports_list)
        print(f"\n[*] Scan Complete. Found {len(open_ports)} open port(s).")
    except KeyboardInterrupt:
        print("\n[!] Scan aborted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Critical framework error: {e}")

if __name__ == "__main__":
    main()


