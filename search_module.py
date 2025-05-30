
import mysql.connector
import local_settings

class SearchModule:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=local_settings.DB_HOST,
                user=local_settings.DB_USER,
                password=local_settings.DB_PASSWORD,
                database=local_settings.DB_DATABASE
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print('\033[31m' + f'Ошибка подключения к базе данных: {err}' + '\033[0m')
            self.conn = None
            self.cursor = None

    def combined_search(self, keyword=None, genre=None, year=None):
        if not self.cursor:
            print('\033[31m' + 'Нет соединения с базой данных.' + '\033[0m')
            return []

        base_query = '''
            SELECT DISTINCT f.title, f.release_year, f.description, c.name AS category
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
        '''
        conditions = []
        params = []

        if keyword:
            conditions.append('f.title LIKE %s')
            params.append(f'%{keyword}%')
        if genre:
            conditions.append('c.name = %s')
            params.append(genre)
        if year:
            conditions.append('f.release_year = %s')
            params.append(year)

        if conditions:
            base_query += ' WHERE ' + ' AND '.join(conditions)

        base_query += ' ORDER BY f.title'

        try:
            self.cursor.execute(base_query, params)
            results = self.cursor.fetchall()
            return results if results else []
        except mysql.connector.Error as err:
            print('\033[31m' + f'Ошибка при выполнении запроса: {err}' + '\033[0m')
            return []

    def get_genres(self):
        if not self.cursor:
            print('\033[31m' + 'Нет соединения с базой данных.' + '\033[0m')
            return []

        try:
            self.cursor.execute('SELECT name FROM category ORDER BY name')
            results = self.cursor.fetchall()
            return [row[0] for row in results] if results else []
        except mysql.connector.Error as err:
            print('\033[31m' + f'Ошибка при получении жанров: {err}' + '\033[0m')
            return []

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()



