from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sqlite3
import time
import os

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                review_rating TEXT,
                review_count TEXT,
                price TEXT,
                seller TEXT,
                installments TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_to_db(self, items):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for item in items:
            cursor.execute('''
                INSERT INTO products (name, review_rating, review_count, price, seller, installments)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (item['Nome'], item['Avaliação'], item['Número de Avaliações'], item['Valor'], item['Vendedor'], item['Parcela']))
        conn.commit()
        conn.close()

class Scraper:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def scrape_mercadolivre(self, term, quantity):
        url = f'https://lista.mercadolivre.com.br/{term}'
        self.driver.get(url)
        items = []
        total_price = 0
        num_items = 0
        time.sleep(5)
        product_elements = self.driver.find_elements(By.CSS_SELECTOR, '.ui-search-results li.ui-search-layout__item .ui-search-result__content-wrapper')
        for product_element in product_elements[:quantity]:
            product_link = product_element.find_element(By.CSS_SELECTOR, '.ui-search-item__group .ui-search-link')
            product_url = product_link.get_attribute("href")
            try:
                installments_element = product_element.find_element(By.CSS_SELECTOR, 'span.ui-search-item__group__element.ui-search-installments')
                installments_text = installments_element.text
            except Exception:
                installments_text = "N/A"
            self.driver.execute_script(f"window.open('{product_url}', '_blank');")
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[1])
            try:
                product_name = self.driver.find_element(By.CLASS_NAME, 'ui-pdp-title').text
            except Exception:
                product_name = "N/A"
            try:
                review_rating = self.driver.find_element(By.CLASS_NAME, 'ui-pdp-review__rating').text
            except Exception:
                review_rating = "N/A"
            try:
                review_count = self.driver.find_element(By.CLASS_NAME, 'ui-pdp-review__amount').text
            except Exception:
                review_count = "N/A"
            try:
                price = self.driver.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text
                total_price += float(price.replace('.', '').replace(',', '.'))
                num_items += 1
            except Exception:
                price = "N/A"
            try:
                seller = self.driver.find_element(By.CLASS_NAME, 'ui-seller-data-header__title-container').text
            except Exception:
                seller = "N/A"
            items.append({
                "Nome": product_name,
                "Avaliação": review_rating,
                "Número de Avaliações": review_count,
                "Valor": price,
                "Vendedor": seller,
                "Parcela": installments_text
            })
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.quit()
        average_price = total_price / num_items if num_items > 0 else 0
        return items, average_price

class WebApp:
    def __init__(self, db_path):
        self.app = Flask(__name__)
        self.db = Database(db_path)
        self.scraper = Scraper()

    def run(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                term = request.form['search']
                quantity = int(request.form['quantity'])
                items, average_price = self.scraper.scrape_mercadolivre(term, quantity)
                self.db.save_to_db(items)
                return render_template('index.html', items=items, average_price=average_price)
            return render_template('index.html', items=[], average_price=0)

        if __name__ == '__main__':
            self.db.init_db()
            self.app.run(debug=True)

if __name__ == '__main__':
    web_app = WebApp('C:\\mercadolivre\\mercadolivre.db')
    web_app.run()
