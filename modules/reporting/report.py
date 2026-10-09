import os
from datetime import datetime

def save_scan_report(target, open_ports=None, discovered_paths=None):
    """Formats and writes toolkit scan findings into a structured log report."""
    # Ensure the outputs directory exists in the root folder
    report_dir = "reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        
    # Generate a unique file name using the target name and current date/time
    clean_target = target.replace("http://", "").replace("https://", "").replace("/", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(report_dir, f"report_{clean_target}_{timestamp}.txt")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=====================================================\n")
        f.write("        🛡️ PENETRATION TESTING ASSESSMENT REPORT\n")
        f.write(f"        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=====================================================\n\n")
        f.write(f"[*] Target Host Profile: {target}\n\n")
        
        # 1. Log Network Port Data if available
        f.write("-----------------------------------------------------\n")
        f.write("🌐 INFRASTRUCTURE PHASE: PORT SCANNER DATA\n")
        f.write("-----------------------------------------------------\n")
        if open_ports is not None:
            f.write(f"[+] Total Open Ports Identified: {len(open_ports)}\n")
            for port in open_ports:
                f.write(f"  - Port {port} is OPEN\n")
        else:
            f.write("[-] Port scan module was not executed during this session.\n")
            
        f.write("\n")
        
        # 2. Log Web Application Data if available
        f.write("-----------------------------------------------------\n")
        f.write("💉 APPLICATION PHASE: WEB DIRECTORY BUSTER DATA\n")
        f.write("-----------------------------------------------------\n")
        if discovered_paths is not None:
            f.write(f"[+] Total Endpoints Discovered: {len(discovered_paths)}\n")
            for path, status in discovered_paths:
                f.write(f"  - /{path} (HTTP Response Status: {status})\n")
        else:
            f.write("[-] Directory busting module was not executed during this session.\n")
            
        f.write("\n=====================================================\n")
        f.write("    End of Security Assessment - Authorized Use Only\n")
        f.write("=====================================================\n")
            
    print(f"\n[+] Comprehensive security brief compiled successfully: {file_path}")
    return file_path
