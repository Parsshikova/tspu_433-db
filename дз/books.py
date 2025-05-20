import requests
from bs4 import BeautifulSoup
import csv
import sqlite3

BASE_URL = "https://books.toscrape.com/"
CSV_FILE = "books.csv"
DB_FILE = "books.db"
NUM_BOOKS_TO_SCRAPE = 5

def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_value TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            availability TEXT,
            description TEXT,
            product_page_url TEXT UNIQUE,
            image_url TEXT,
            category_id INTEGER,
            upc TEXT UNIQUE,
            date_id INTEGER,
            tags TEXT,
            author TEXT
        )
    """)
    conn.commit()
    conn.close()
def write_to_csv(data):   
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'price', 'availability', 'description', 'product_page_url', 'image_url', 'category', 'upc']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def load_csv_to_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT OR IGNORE INTO categories (name) VALUES (?)
            """, (row['category'],))
            cursor.execute("SELECT id FROM categories WHERE name = ?", (row['category'],))
            category_id = cursor.fetchone()[0]

            
            tags_value = row.get('tags', '')

            cursor.execute("""
    INSERT OR IGNORE INTO books (title, price, availability, description, product_page_url, image_url, category_id, upc, tags, author)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    row['title'],
    row['price'],
    row['availability'],
    row['description'],
    row['product_page_url'],
    row['image_url'],
    category_id,
    row['upc'],
    row.get('tags', ''),
    row.get('author', 'Unknown')
))
    conn.commit()
    conn.close()

def parse_book_details(book_url):
    """Парсит детали книги, включая автора."""
    try:
        response = requests.get(book_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1').text.strip()
        price = float(soup.find('p', class_='price_color').text[1:])
        availability = soup.find('p', class_='instock availability').text.strip()
        description_tag = soup.find('article', class_='product_page').find('p', recursive=False)
        description = description_tag.text.strip() if description_tag else 'No description available'
        image_url = BASE_URL + soup.find('img').get('src').replace('../..', '').lstrip('/')
        category = soup.find("ul", class_="breadcrumb").find_all('a')[2].text
        upc = soup.find('table', class_='table').find_all('tr')[0].find('td').text

       
        author = "Unknown"  
        
        author_tag = soup.find('th', string='Author')
        if author_tag:
            author = author_tag.find_next_sibling('td').text.strip()

        return {
            'title': title,
            'price': price,
            'availability': availability,
            'description': description,
            'product_page_url': book_url,
            'image_url': image_url,
            'category': category,
            'upc': upc,
            'author': author
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {book_url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing {book_url}: {e}")
        return None
def scrape_books(num_books):
    """Scrapes book listings and their details from multiple pages."""
    books_data = []
    page_num = 1
    books_scraped =0
    while books_scraped < num_books:
        url = f"{BASE_URL}catalogue/page-{page_num}.html"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            book_listings = soup.find_all('article', class_='product_pod')

            if not book_listings:  
                print("No more book listings found.")
                break

            for listing in book_listings:
                if books_scraped >= num_books:
                    break

                book_url = BASE_URL + 'catalogue/' + listing.find('a').get('href').replace('../../../', '') 

                book_details = parse_book_details(book_url)
                if book_details:
                    books_data.append(book_details)
                    books_scraped += 1
                    print(f"Scraped book {books_scraped}/{num_books}: {book_details['title']}")
                else:
                    print(f"Failed to scrape details for {book_url}")

            page_num += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            break 
        except Exception as e:
            print(f"Error parsing main page {url}: {e}")
            break 

    print(f"Successfully scraped {len(books_data)} books.")
    return books_data

if __name__ == "__main__":
    create_database()  
    books = scrape_books(NUM_BOOKS_TO_SCRAPE) 
    write_to_csv(books)  
    load_csv_to_db() 
    print("Data scraping, CSV writing, and database loading complete.")
