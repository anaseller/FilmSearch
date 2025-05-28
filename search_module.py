

import mysql.connector
import local_settings

class SearchModule:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=local_settings.DB_HOST,
            user=local_settings.DB_USER,
            password=local_settings.DB_PASSWORD,
            database=local_settings.DB_DATABASE
        )
        self.cursor = self.conn.cursor()

    def combined_search(self, keyword=None, genre=None, year=None):
        query = '''
            SELECT DISTINCT f.title, f.release_year, f.description, c.name AS category
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            WHERE 1=1
        '''
        params = []

        if keyword:
            query += ' AND f.title LIKE %s'
            params.append(f'%{keyword}%')
        if genre:
            query += ' AND c.name = %s'
            params.append(genre)
        if year:
            query += ' AND f.release_year = %s'
            params.append(year)

        query += ' ORDER BY f.title'
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_genres(self):
        self.cursor.execute('SELECT name FROM category ORDER BY name')
        return [row[0] for row in self.cursor.fetchall()]

    def close(self):
        self.cursor.close()
        self.conn.close()

