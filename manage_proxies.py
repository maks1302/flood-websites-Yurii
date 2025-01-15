import os
import zipfile
import random
from selenium import webdriver
from extention import background_js, manifest_json


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

# Create extensions directory if it doesn't exist

def get_proxy(mobile_browser):
    """
    Configure and return a Chrome WebDriver instance with proxy authentication
    """
    # Generate proxy authentication background script
    proxy_background = background_js % (parse_proxy())
    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    if mobile_browser.lower() == 'y':
        chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})
    
    # Create and load proxy authentication extension
    extension_path = os.path.join(EXTENSIONS_DIR, 'proxy_auth_plugin.zip')
    with zipfile.ZipFile(extension_path, 'w') as zip_file:
        zip_file.writestr("manifest.json", manifest_json)
        zip_file.writestr("background.js", proxy_background)
    
    # Add extension to Chrome options
    chrome_options.add_extension(extension_path)
    # chrome_options.add_argument(f'user-agent={user_agent}')
    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # chrome_options.add_argument("--incognito")
    # Initialize and return WebDriver
    return chrome_options
