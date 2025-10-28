import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class EmexParser:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini')
        self.username = self.config.get('emex.ru', 'username')
        self.password = self.config.get('emex.ru', 'password')

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            options=chrome_options
        )
        self.login()

    def login(self):
        self.driver.get('https://www.emex.ru/login')  # Assuming this is the login URL
        username_field = self.driver.find_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')

        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)

        # Wait for login to complete
        # A proper implementation would wait for a specific element to appear
        print("Successfully logged in to emex.ru")

    def search_by_vin(self, vin):
        self.driver.get('https://www.emex.ru/products/search') # Assuming this is the search page
        search_box = self.driver.find_element(By.ID, 'vin-search-input') # Assuming the id of the search box
        search_box.send_keys(vin)
        search_box.send_keys(Keys.RETURN)

        # A proper implementation would wait for the results to load
        return self.parse_results()

    def parse_results(self):
        results = []
        # Assuming search results are in a table with a specific class
        result_rows = self.driver.find_elements(By.CSS_SELECTOR, 'tr.search-result')

        for row in result_rows:
            name = row.find_element(By.CSS_SELECTOR, 'td.name').text
            part_number = row.find_element(By.CSS_SELECTOR, 'td.part-number').text
            brand = row.find_element(By.CSS_SELECTOR, 'td.brand').text
            price = row.find_element(By.CSS_SELECTOR, 'td.price').text
            link = row.find_element(By.TAG_NAME, 'a').get_attribute('href')
            results.append({
                'name': name,
                'part_number': part_number,
                'brand': brand,
                'price': price,
                'link': link
            })
        return results

    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    parser = EmexParser()
    # Example usage:
    # results = parser.search_by_vin('some_vin_code')
    # print(results)
    parser.close()
