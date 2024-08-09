from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set the path to your webdriver executable
webdriver_path = './chromedriver'

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')  # Optional: Run in headless mode

# Specify the executable path in the options
chrome_options.binary_location = webdriver_path

# Create a new instance of the Chrome driver with options
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the target website
driver.get('http://www.openrice.com/en/hongkong/restaurant/sr1.htm?tc=sr1quick&s=1&region=0&inputstrwhat=&inputstrwhere=&district_id=3015')

# Perform scraping actions
# (interact with elements, retrieve data, etc.)
def scrape():
    elements = driver.find_elements(By.CLASS_NAME, 'poi-list-cell-wrapper')
    for element in elements:
        restaurant = element.find_element(By.CLASS_NAME, 'poi-list-cell-desktop-right-top-info-section')
        rest = restaurant.find_element(By.CLASS_NAME, 'text')
        name = rest.text
        link = rest.find_elements(By.XPATH, './/a')
        link = link[0].get_attribute('href')
        info = restaurant.find_element(By.CLASS_NAME, 'poi-list-cell-line-info')
        address = info.find_element(By.XPATH,'.//div')
        address = address.text
        details = restaurant.find_element(By.CLASS_NAME, 'poi-list-cell-line-info-details')
        cuisines = details.find_elements(By.XPATH, './/a')
        if len(cuisines) == 0:
            district = 'N/A'
            style = 'N/A'
            dish = 'N/A'
        elif len(cuisines) == 1:
            district = cuisines[0].text
            style = 'N/A'
            dish = 'N/A'
        elif len(cuisines) == 2:
            district = cuisines[0].text
            style = cuisines[1].text
            dish = 'N/A'
        elif len(cuisines) == 3:
            district = cuisines[0].text
            style = cuisines[1].text
            dish = cuisines[2].text
        price = details.find_element(By.CLASS_NAME, 'price')
        price = price.text
        with open('openrice.txt', 'a+') as f:
            f.seek(0, 2)  # Move the cursor to the end of the file
            is_empty = f.tell() == 0
            if is_empty:
                f.write('Style|Dish|Price|Name|Address|Link\n')
            f.write(f'{district.replace("/","").strip()}|{style.replace("/","")}|{dish}|{price.replace("/","")}|{name}|{address.replace(",","")}|{link}\n')
for n in range(20):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
scrape()


# Close the browser window
# driver.quit()

