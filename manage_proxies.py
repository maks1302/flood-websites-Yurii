import os
import zipfile
import random
from selenium import webdriver
from extention import background_js, manifest_json


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
PROXY_FILE = 'proxy.txt'

try:
    with open(PROXY_FILE, 'r') as f:
        proxy_lines = f.readlines()
        proxy_str = random.choice([line for line in proxy_lines if line.strip()])
        PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD = parse_proxy_string(proxy_str)
except FileNotFoundError:
    pass
# Create extensions directory if it doesn't exist
EXTENSIONS_DIR = 'extentions'
if not os.path.exists(EXTENSIONS_DIR):
    os.makedirs(EXTENSIONS_DIR)


def get_proxy():
    """
    Configure and return a Chrome WebDriver instance with proxy authentication
    """
    # Generate proxy authentication background script
    proxy_background = background_js % (PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD)
    
    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    
    # Create and load proxy authentication extension
    extension_path = os.path.join(EXTENSIONS_DIR, 'proxy_auth_plugin.zip')
    with zipfile.ZipFile(extension_path, 'w') as zip_file:
        zip_file.writestr("manifest.json", manifest_json)
        zip_file.writestr("background.js", proxy_background)
    
    # Add extension to Chrome options
    chrome_options.add_extension(extension_path)
    
    # Initialize and return WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    return driver
