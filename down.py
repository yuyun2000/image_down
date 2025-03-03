import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.exceptions import RequestException

# Set up the Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless to avoid opening a browser window
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

print("Set up the Selenium WebDriver")
# URL of the website
url = "https://500px.com.cn/community/set/fe124cfe5b0e4740853c35f99bdb26fb/details?swipe=1&rs=240e3e1b34b008b2809fda2e60f209365"
name = "data11"

# Open the URL
driver.get(url)
print("Open the URL")

# Wait for the page to load completely
time.sleep(1)
print("Wait for the page to load completely")

# Scroll down to load more images
scroll_pause_time = 1  # Pause time between scrolls
scroll_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    
    # Calculate new scroll height and compare with the last scroll height
    new_scroll_height = driver.execute_script("return document.body.scrollHeight")
    if new_scroll_height == scroll_height:
        break
    scroll_height = new_scroll_height

print("Scroll down to load more images")

# After scrolling, parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all image tags
images = soup.find_all("img")

# Set up the folder to save images
download_folder = "images"
os.makedirs(download_folder, exist_ok=True)

# Function to check if an image URL is valid
def is_valid_image(url):
    try:
        response = requests.head(url, allow_redirects=True)
        # Check if the response content type is an image
        if 'image' in response.headers.get('Content-Type', ''):
            return True
    except RequestException as e:
        print(f"Error with URL {url}: {e}")
    return False

# Download each image
for idx, img in enumerate(images):
    try:
        # Get the image URL from the 'data-src' or 'src' attribute
        img_url = img.get("data-src") or img.get("src")
        
        if img_url:
            # Handle relative URLs by joining with the base URL
            img_url = urljoin(url, img_url)
            
            # Check if the image URL is valid before attempting to download
            if not is_valid_image(img_url):
                print(f"Skipping invalid image URL {img_url}")
                continue
            
            # Request the image
            img_response = requests.get(img_url)
            
            # Verify the response before saving the image
            if img_response.status_code == 200 and 'image' in img_response.headers['Content-Type']:
                img_name = f"{download_folder}/{name}_{idx+1}.jpg"
                with open(img_name, "wb") as f:
                    f.write(img_response.content)
                print(f"Downloaded {img_name}")
            else:
                print(f"Error downloading image {img_url}: Invalid response")
        else:
            print(f"Skipping image {idx+1}: No valid image URL")
    except Exception as e:
        print(f"Error downloading image {idx+1}: {e}")

# Close the Selenium WebDriver
driver.quit()