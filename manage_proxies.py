import os
import random
from selenium import webdriver


EXTENSIONS_DIR = 'extentions'
if not os.path.exists(EXTENSIONS_DIR):
    os.makedirs(EXTENSIONS_DIR)

def parse_proxy_string(proxy_str):
    """
    Parse proxy string in format host:port:username:password
    """
    try:
        host, port, username, password = proxy_str.strip().split(':')
        return host, port, username, password
    except ValueError:
        raise ValueError("Proxy string must be in format 'host:port:username:password'")


# Load proxy configuration from txt file

def parse_proxy():
    try:
        PROXY_FILE = 'proxy.txt'
        with open(PROXY_FILE, 'r') as f:
            proxy_lines = f.readlines()
            proxy_str = random.choice([line for line in proxy_lines if line.strip()])
            PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD = parse_proxy_string(proxy_str)
            return PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD
    except FileNotFoundError:
        return None

def get_proxy(mobile_browser):
    """
    Build Chrome options and selenium-wire proxy options for authenticated HTTP proxies.
    Returns: (chrome_options, seleniumwire_options)
    """
    creds = parse_proxy()
    chrome_options = webdriver.ChromeOptions()
    if mobile_browser.lower() == 'y':
        chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})

    if not creds:
        # No proxy file found or empty; return options without proxy
        return chrome_options, {}

    PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD = creds

    proxy_url = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
    seleniumwire_options = {
        'proxy': {
            'http': proxy_url,
            'https': proxy_url,
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    # You can still add other Chrome flags here if needed, but proxy auth is handled by selenium-wire.
    return chrome_options, seleniumwire_options
