import requests
import concurrent.futures

def check_directory(target_url, path):
    """Checks if a specific path exists on the web server."""
    if not target_url.startswith(('http://', 'https://')):
        target_url = f"http://{target_url}"
        
    url = f"{target_url.rstrip('/')}/{path.lstrip('/')}"
    try:
        response = requests.get(url, timeout=3, allow_redirects=False)
        
        # Check standard successful, redirected, or protected status codes directly
        status = response.status_code
        if (status == 200) or (status == 301) or (status == 302) or (status == 403):
            return path, status
    except requests.RequestException:
        return None
    return None

def run_dir_brute(target_url, custom_wordlist=None):
    """Runs a fast parallel check across common web paths."""
    print(f"\n[*] Launching Directory Buster against: {target_url}")
    
    wordlist = custom_wordlist or [
        "admin", "login", "config.php", ".env", "backup", 
        "api", "wp-admin", "robots.txt", "uploads", "dashboard",
        "secret", "db", "administrator", "assets", "test"
    ]
    
    discovered_paths = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_directory, target_url, path): path for path in wordlist}
        
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                path, status = res
                print(f" [+] Found Endpoint: /{path} (Status: {status})")
                discovered_paths.append((path, status))
                
    if not discovered_paths:
        print(" [-] No hidden web paths discovered via standard wordlist.")
    return discovered_paths
