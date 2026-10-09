import socket
import concurrent.futures

def scan_single_port(target_host, port):
    """Attempts to connect to a specific port on the target host."""
    try:
        # Create a stream socket using TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0) # Stop waiting after 1 second
            result = s.connect_ex((target_host, port))
            if result == 0:
                return port
    except Exception:
        return None
    return None

def run_port_scan(target_host, ports_to_scan=[21, 22, 23, 25, 53, 80, 443, 8080]):
    """Scans multiple ports concurrently using a thread pool."""
    print(f"\n[*] Launching Port Scan against: {target_host}")
    open_ports = []
    
    # Use thread pools to scan multiple ports simultaneously
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Map out the single port scan function across the target ports
        futures = {executor.submit(scan_single_port, target_host, port): port for port in ports_to_scan}
        
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            try:
                open_port = future.result()
                if open_port:
                    print(f" [+] Port {open_port} is OPEN")
                    open_ports.append(open_port)
            except Exception as e:
                print(f" [!] Error scanning port {port}: {e}")
                
    if not open_ports:
        print(" [-] No open ports discovered in the target range.")
    return open_ports
