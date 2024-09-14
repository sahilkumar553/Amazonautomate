from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import traceback

# Path to your ChromeDriver executable
driver_path = "D:/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # Update the path as needed

def setup_driver():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=options)

def random_sleep(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def wait_and_click(driver, by, value, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    random_sleep(1, 2)
    ActionChains(driver).move_to_element(element).click().perform()
    random_sleep(2, 3)

def search_and_add_to_cart():
    driver = setup_driver()
    try:
        # Open Amazon
        driver.get("https://www.amazon.in")
        print("Opened Amazon")
        random_sleep(2, 4)
        
        # Search for laptops
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_box.send_keys("laptops")
        random_sleep(0.5, 1)
        search_box.submit()
        print("Search submitted")
        
        # Wait for search results to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
        )
        random_sleep(2, 4)
        
        # Click on the first product
        wait_and_click(driver, By.CSS_SELECTOR, "div.s-main-slot div.s-result-item h2 a")
        print("First product clicked")
        
        # Wait for product page to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            )
            print("Product page loaded")
        except TimeoutException:
            print("Timeout waiting for product page. Current URL:", driver.current_url)
            driver.save_screenshot("product_page_timeout.png")
            raise
        
        # Add to cart functionality
        wait_and_click(driver, By.ID, "add-to-cart-button")
        print("Product added to the cart")
        
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        print(f"Current URL: {driver.current_url}")
    except TimeoutException as e:
        print(f"Timeout waiting for element: {e}")
        print(f"Current URL: {driver.current_url}")
    except WebDriverException as e:
        print(f"WebDriver exception: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())
    finally:
        # Take a screenshot before closing
        driver.save_screenshot("final_state.png")
        print("Screenshot saved as final_state.png")
        
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    search_and_add_to_cart()