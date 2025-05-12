# main.py

from test import (
    get_by_tags,
    get_by_authors,
    get_author_count_quotes,
    get_top_authors,
    get_top_tags,
    get_author_tags,
    get_avg_book_price,
    get_low_books
)

def main():
    print("=== Получение книг по тегам ===")
    tags = ["mystery", "adventure"]
    books_by_tags = get_by_tags(tags)
    for book in books_by_tags:
        print(f"Title: {book['title']}, Tags: {book['tags']}")

    print("\n=== Получение книг по авторам ===")
    authors = ["Author Name"]
    books_by_authors = get_by_authors(authors)
    for book in books_by_authors:
        print(f"Title: {book['title']}, Author: {book.get('author')}")

    print("\n=== Количество книг у автора ===")
    author_name = "Author Name"
    count = get_author_count_quotes(author_name)
    print(f"Количество книг у {author_name}: {count}")

    print("\n=== Топ авторов ===")
    top_authors = get_top_authors(limit=3)
    print("Топ авторов:", top_authors)

    print("\n=== Топ тегов ===")
    top_tags = get_top_tags(limit=3)
    print("Топ тегов:", top_tags)

    print("\n=== Теги автора ===")
    author_name = "Author Name"
    tags_of_author = get_author_tags(author_name)
    print(f"Теги автора {author_name}:", tags_of_author)

    print("\n=== Средняя цена книг автора ===")
    avg_price = get_avg_book_price(author_name)
    print(f"Средняя цена книг {author_name}: {avg_price}")

    print("\n=== Книги с низким остатком ===")
    low_stock_books = get_low_books(limit=3)
    for book in low_stock_books:
        print(f"Title: {book['title']}, Остаток: {book['stock_count']}")

if __name__ == "__main__":
    main()