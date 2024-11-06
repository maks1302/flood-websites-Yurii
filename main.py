from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import random
from manage_proxies import get_proxy
import logging

def setup_logging():
    logger = logging.getLogger('bot_logger')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File handler for logging to file
    file_handler = logging.FileHandler('bot_log.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def log_and_print(message, level='info'):
    """Helper function to both log and print messages"""
    logger = logging.getLogger('bot_logger')
    print(message)  # Print to console only
    
    # Log to file only
    if level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)

def get_websites():
    try:
        with open('websites.txt', 'r') as f:
            websites = [line.strip() for line in f if line.strip()]
            if not websites:
                # Fallback if file is empty
                return ["https://example.com/"]
            return websites
    except FileNotFoundError:
        log_and_print("Warning: websites.txt not found, using default websites", 'warning')
        return ["https://example.com/"]
            
def get_button_texts():
    try:
        with open('buttons.txt', 'r', encoding='utf-8') as f:
            button_texts = [line.strip() for line in f if line.strip()]
            return button_texts
    except FileNotFoundError:
        log_and_print("Warning: button_texts.txt not found, using default button texts", 'warning')
        return ["придбати зараз", "замовити зараз"]

def get_random_name():
    first_name = ""
    last_name = ""
    
    # Read first name
    try:
        with open('first_names.txt', 'r', encoding='utf-8') as f:
            first_names = [line.strip() for line in f if line.strip()]
            if first_names:
                first_name = random.choice(first_names)
    except FileNotFoundError:
        log_and_print("Warning: first_names.txt not found", 'warning')
        
    # Read last name
    try:
        with open('last_names.txt', 'r', encoding='utf-8') as f:
            last_names = [line.strip() for line in f if line.strip()]
            if last_names:
                last_name = random.choice(last_names)
    except FileNotFoundError:
        log_and_print("Warning: last_names.txt not found", 'warning')

    if first_name and last_name:
        return f"{first_name} {last_name}"
    elif first_name:
        return first_name
    elif last_name:
        return last_name
    else:
        return "Марія Ященко"  # Fallback if no names are available

def get_random_phone():
    try:
        with open('phone_numbers.txt', 'r') as f:
            phone_numbers = [line.strip() for line in f if line.strip()]
            if phone_numbers:
                return random.choice(phone_numbers)
    except FileNotFoundError:
        log_and_print("Warning: phone_numbers.txt not found", 'warning')
        return "+380994556191"  # Fallback if file not found
    return "+380994556191"  # Fallback if file is empty


def get_random_city():
    try:
        with open('cities.txt', 'r', encoding='utf-8') as f:
            cities = [line.strip() for line in f if line.strip()]
            if cities:
                return random.choice(cities)
    except FileNotFoundError:
        log_and_print("Warning: cities.txt not found", 'warning')
        return "Київ"  # Fallback if file not found
    return "Київ"  # Fallback if file is empty


def fill_search_fields(wait_minutes):
    setup_logging()  # Initialize logging
    while True:
        try:
            log_and_print("\nStarting new cycle...")
            driver = get_proxy()
            
            websites = get_websites()
            remaining_sites = websites.copy()
            
            while remaining_sites:
                site = random.choice(remaining_sites)
                remaining_sites.remove(site)
                
                try:
                    random_name = get_random_name()
                    radnom_city = get_random_city()
                    driver.get(site)
                    wait = WebDriverWait(driver, 10)
                    
                    # Simulate natural scrolling
                    time.sleep(random.uniform(1, 2))
                    driver.execute_script("window.scrollBy(0, 400);")
                    time.sleep(random.uniform(0.5, 1))
                    
                    # Handle dropdowns
                    try:
                        select_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "select")))
                        for select_element in select_elements:
                            select = Select(select_element)
                            options = select.options
                            for option in options:
                                if "обрати" in option.text.lower():
                                    valid_options = [opt for opt in options if "обрати" not in opt.text.lower()]
                                    if valid_options:
                                        random_option = random.choice(valid_options)
                                        select.select_by_visible_text(random_option.text)
                                        log_and_print(f"Selected option '{random_option.text}' from dropdown on: {site}")
                                    break
                    except Exception as e:
                        log_and_print(f"No select elements found or error handling selects on {site}: {e}", 'error')
                                        
                    # Fill city field
                    try:
                        city_field = wait.until(EC.presence_of_element_located(
                            (By.XPATH, "//input[@type='text' and @name='city']")))
                        city_field.clear()
                        print(radnom_city)
                        for char in radnom_city:
                            city_field.send_keys(char)
                            time.sleep(random.uniform(0.1, 0.2))
                        log_and_print(f"Filled city field on: {site}")
                    except Exception as e:
                        log_and_print(f"Could not find or fill city field on {site}: {e}", 'error')

                    # Fill name field
                    try:
                        name_field = wait.until(EC.presence_of_element_located(
                            (By.XPATH, "//input[@type='text' and (@name='name' or @name='username' or @name='Name')]")))
                        name_field.clear()
                        for char in random_name:
                            name_field.send_keys(char)
                            time.sleep(random.uniform(0.1, 0.2))
                        log_and_print(f"Filled name field on: {site}")
                    except Exception as e:
                        log_and_print(f"Could not find or fill name field on {site}: {e}", 'error')
                        
                    # Fill phone field    
                    try:
                        phone_field = wait.until(EC.presence_of_element_located(
                            (By.XPATH, "//input[translate(@type,'TEL','tel')='tel']")))
                        phone_field.clear()
                        phone = get_random_phone()
                        for char in phone:
                            phone_field.send_keys(char)
                            time.sleep(random.uniform(0.1, 0.2))
                        log_and_print(f"Filled phone field on: {site}")
                    except Exception as e:
                        log_and_print(f"Could not find or fill phone field on {site}: {e}", 'error')
                        
                    # Click the button below the filled fields
                    try:
                        # Find the button element that appears after the input fields
                        button = wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//input[@type='tel']/following::button[1]")
                            )
                        )
                        time.sleep(random.uniform(0.5, 1))
                        driver.execute_script("arguments[0].click();", button)
                        log_and_print(f"Clicked button on: {site}")
                    except Exception as e:
                        log_and_print(f"Could not find or click button on {site}: {e}", 'error')
                    
                    time.sleep(random.uniform(5, 10))
                    
                except Exception as e:
                    log_and_print(f"Error processing {site}: {e}", 'error')
                    
            driver.quit()
            log_and_print("Cycle completed! Waiting before starting next cycle...")

            min_wait = wait_minutes * 60 * 0.8
            max_wait = wait_minutes * 60 * 1.2
            cycle_delay = random.uniform(min_wait, max_wait)
            log_and_print(f"Waiting {cycle_delay/60:.2f} minutes until next cycle...")
            time.sleep(cycle_delay)
            
        except Exception as e:
            log_and_print(f"Error during cycle: {e}", 'error')
            time.sleep(10)

if __name__ == "__main__":
    log_and_print("Starting continuous website processing...")
    try:
        wait_minutes = float(input("Enter wait interval between cycles in minutes: "))
        fill_search_fields(wait_minutes)
    except KeyboardInterrupt:
        log_and_print("\nProgram terminated by user.")