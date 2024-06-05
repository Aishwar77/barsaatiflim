import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pymongo import MongoClient
from datetime import datetime
import uuid


def get_trending_topics():
    # Proxy settings (optional)
    proxy = 'us-ca.proxymesh.com:31280'  # Replace with your ProxyMesh details if needed
    edge_options = webdriver.EdgeOptions()
    if proxy:
        edge_options.add_argument(f'--proxy-server={proxy}')

    # Set up WebDriver
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.get('https://twitter.com/login')

    # Log in to Twitter
    username = 'A_k_official125'
    password = 'KSAA277$'

    # Wait for username input to be present
    wait = WebDriverWait(driver, 15)
    user_input = wait.until(EC.presence_of_element_located((By.NAME, 'text')))
    user_input.send_keys(username)
    user_input.send_keys(Keys.RETURN)

    # Wait for password input to be present
    pass_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.RETURN)

    # Wait for login to complete
    home_loaded = wait.until(
        EC.presence_of_element_located((By.XPATH, "//section[contains(@aria-labelledby, 'accessible-list-0')]")))
    time.sleep(5)  # Additional wait for the trending section to load completely

    # Fetch trending topics
    trending_section = wait.until(
        EC.presence_of_element_located((By.XPATH, "//section[contains(@aria-labelledby, 'accessible-list-0')]")))
    trends = trending_section.find_elements(By.XPATH, ".//span[contains(text(), '#')]")

    top_trends = [trend.text for trend in trends[:5]]

    # Fetch IP address
    ip_address = requests.get('http://ipinfo.io/ip').text.strip()

    # Store data in MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.twitter_trends
    collection = db.trends

    unique_id = str(uuid.uuid4())
    end_time = datetime.now()

    document = {
        'unique_id': unique_id,
        'trend1': top_trends[0],
        'trend2': top_trends[1],
        'trend3': top_trends[2],
        'trend4': top_trends[3],
        'trend5': top_trends[4],
        'end_time': end_time,
        'ip_address': ip_address
    }

    collection.insert_one(document)

    driver.quit()

    return document


# Example usage
if __name__ == '__main__':
    print(get_trending_topics())
