import configparser
import requests
from bs4 import BeautifulSoup

class LeoparParser:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini')
        self.username = self.config.get('leopar.kz', 'username')
        self.password = self.config.get('leopar.kz', 'password')
        self.session = requests.Session()
        self.login()

    def login(self):
        login_url = 'https://leopar.kz/login'  # Assuming this is the login URL
        login_data = {
            'username': self.username,
            'password': self.password
        }
        response = self.session.post(login_url, data=login_data)
        if response.status_code == 200:
            print("Successfully logged in to leopar.kz")
        else:
            print("Failed to log in to leopar.kz")

    def search_by_vin(self, vin):
        search_url = f'https://leopar.kz/search?vin={vin}'  # Assuming this is the search URL
        response = self.session.get(search_url)
        if response.status_code == 200:
            return self.parse_results(response.text)
        else:
            print(f"Failed to search for VIN {vin} on leopar.kz")
            return None

    def parse_results(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        # Assuming the search results are in a table with a specific class
        for row in soup.find_all('tr', class_='search-result'):
            name = row.find('td', class_='name').text
            part_number = row.find('td', class_='part-number').text
            brand = row.find('td', class_='brand').text
            price = row.find('td', class_='price').text
            link = row.find('a')['href']
            results.append({
                'name': name,
                'part_number': part_number,
                'brand': brand,
                'price': price,
                'link': link
            })
        return results

if __name__ == '__main__':
    parser = LeoparParser()
    # Example usage:
    # results = parser.search_by_vin('some_vin_code')
    # print(results)
