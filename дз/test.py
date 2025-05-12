from typing import List
import sqlite3

DB_FILE = "books.db"

def get_by_tags(tags: List[str] = None) -> List:
    """
    Получение записей по тегам.
    Возвращает список словарей книг, у которых есть хотя бы один из указанных тегов.
    """
    if tags is None:
        tags = []
    results = []
    if not tags:
        return results
    placeholders = ','.join('?' for _ in tags)
    query = f"""
        SELECT b.* FROM books b
        WHERE {" OR ".join([f"tags LIKE '%' || ? || '%'" for _ in tags])}
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, tags)
        rows = cursor.fetchall()
        # Получим имена колонок
        col_names = [desc[0] for desc in cursor.description]
        for row in rows:
            results.append(dict(zip(col_names, row)))
    return results

def get_by_authors(authors: List[str] = None) -> List:
    """
    Получение записей по авторам.
    """
    if authors is None:
        return []
    results = []
    placeholders = ','.join('?' for _ in authors)
    query = f"""
        SELECT * FROM books
        WHERE author IN ({placeholders})
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, authors)
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        for row in rows:
            results.append(dict(zip(col_names, row)))
    return results

def get_author_count_quotes(author: str = None) -> int:
    """
    Количество книг у автора.
    """
    if not author:
        return 0
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books WHERE author = ?", (author,))
        count = cursor.fetchone()[0]
    return count

def get_top_authors(limit: int = 5) -> List:
    """
    Топ авторов по количеству книг.
    Возвращает список кортежей (author, count).
    """
    results = []
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT author, COUNT(*) as cnt
            FROM books
            GROUP BY author
            ORDER BY cnt DESC
            LIMIT ?
        """, (limit,))
        for row in cursor.fetchall():
            results.append({'author': row[0], 'book_count': row[1]})
    return results

def get_top_tags(limit: int = 5) -> List:
    """
    Топ тегов по частоте.
    Предполагается, что tags — строка, разделенная запятыми или пробелами.
    Для простоты разделим по запятой и пробелам.
    """
    tag_counts = {}
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tags FROM books WHERE tags IS NOT NULL")
        rows = cursor.fetchall()
        for (tags_str,) in rows:
            if tags_str:
                # Разделим по запятой и пробелам
                tags_list = [tag.strip() for tag in tags_str.replace(',', ' ').split()]
                for tag in tags_list:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
    # Отсортируем по убыванию частоты
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    return [{'tag': tag, 'count': count} for tag, count in sorted_tags[:limit]]

def get_author_tags(author: str = None):
    """
    Список тегов, используемых автором.
    """
    if not author:
        return []
    tags_counter = {}
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tags FROM books WHERE author = ?", (author,))
        rows = cursor.fetchall()
        for (tags_str,) in rows:
            if tags_str:
                tags_list = [tag.strip() for tag in tags_str.replace(',', ' ').split()]
                for tag in tags_list:
                    tags_counter[tag] = tags_counter.get(tag, 0) + 1
    return list(tags_counter.keys())

def get_avg_book_price(author: str) -> float:
    """
    Средняя цена книг автора.
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(price) FROM books WHERE author = ?", (author,))
        result = cursor.fetchone()[0]
        if result is None:
            return 0.0
        return float(result)

def get_low_books(limit: int = 5) -> List:
    """
    Книги с низким остатком. Предполагается, что у вас есть поле stock_count,
    но в вашей схеме его нет. Если у вас есть поле stock_count, используйте его.
    В текущей схеме его нет, поэтому я сделаю предположение, что есть поле 'availability' 
    или добавлю пример с использованием этого поля (если есть).
    """
    # Предположим, что есть поле 'availability' с текстом: 'In stock (5 available)'.
    # Тогда можно парсить число.
    results = []
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        for row in rows:
            row_dict = dict(zip(col_names, row))
            # Попытка извлечь число из 'availability'
            avail_text = row_dict.get('availability', '')
            import re
            match = re.search(r'(\d+)', avail_text)
            count = int(match.group(1)) if match else None
            if count is not None and count <= limit:
                results.append(row_dict)
        # Можно отсортировать по количеству
        results.sort(key=lambda x: int(re.search(r'(\d+)', x.get('availability', '')).group(1) if re.search(r'(\d+)', x.get('availability', '')) else 0))
        return results[:limit]