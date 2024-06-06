from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sqlite3
import time
import os

app = Flask(__name__)

def init_db():
    # Define the path for the database
    db_dir = 'C:\\mercadolivre'
    db_path = os.path.join(db_dir, 'mercadolivre.db')

    # Create the directory if it does not exist
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Create a database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a table if it doesn't exist
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

def save_to_db(items):
    db_path = 'C:\\mercadolivre\\mercadolivre.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for item in items:
        cursor.execute('''
            INSERT INTO products (name, review_rating, review_count, price, seller, installments)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (item['Nome'], item['Avaliação'], item['Número de Avaliações'], item['Valor'], item['Vendedor'], item['Parcela']))
    
    conn.commit()
    conn.close()

def scrape_mercadolivre(term, quantity):
    url = f'https://lista.mercadolivre.com.br/{term}'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    items = []
    total_price = 0
    num_items = 0

    time.sleep(5)

    product_elements = driver.find_elements(By.CSS_SELECTOR, '.ui-search-results li.ui-search-layout__item .ui-search-result__content-wrapper')

    for product_element in product_elements[:quantity]:
        product_link = product_element.find_element(By.CSS_SELECTOR, '.ui-search-item__group .ui-search-link')
        product_url = product_link.get_attribute("href")

        try:
            installments_element = product_element.find_element(By.CSS_SELECTOR, 'span.ui-search-item__group__element.ui-search-installments')
            installments_text = installments_element.text
        except Exception:
            installments_text = "N/A"

        driver.execute_script(f"window.open('{product_url}', '_blank');")
        time.sleep(3)

        driver.switch_to.window(driver.window_handles[1])

        try:
            product_name = driver.find_element(By.CLASS_NAME, 'ui-pdp-title').text
        except Exception:
            product_name = "N/A"

        try:
            review_rating = driver.find_element(By.CLASS_NAME, 'ui-pdp-review__rating').text
        except Exception:
            review_rating = "N/A"

        try:
            review_count = driver.find_element(By.CLASS_NAME, 'ui-pdp-review__amount').text
        except Exception:
            review_count = "N/A"

        try:
            price = driver.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text
            total_price += float(price.replace('.', '').replace(',', '.'))
            num_items += 1
        except Exception:
            price = "N/A"

        try:
            seller = driver.find_element(By.CLASS_NAME, 'ui-seller-data-header__title-container').text
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

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    driver.quit()

    average_price = total_price / num_items if num_items > 0 else 0

    save_to_db(items)

    return items, average_price

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        term = request.form['search']
        quantity = int(request.form['quantity'])
        items, average_price = scrape_mercadolivre(term, quantity)
        return render_template('index.html', items=items, average_price=average_price)
    return render_template('index.html', items=[], average_price=0)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
