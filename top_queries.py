

import mysql.connector
import local_settings
from datetime import datetime

class TopQueries:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=local_settings.DB_HOST,
                user=local_settings.DB_USER,
                password=local_settings.DB_PASSWORD,
                database=local_settings.DB_DATABASE
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print('\033[31m' + f'Ошибка подключения к базе данных: {err}' + '\033[0m')
            self.conn = None
            self.cursor = None

    def log_query(self, keyword, genre, year):
        if not self.cursor:
            return
        query = '''
            INSERT INTO search_results (keyword, genre, year, search_time)
            VALUES (%s, %s, %s, %s)
        '''
        now = datetime.now()
        try:
            self.cursor.execute(query, (keyword, genre, year, now))
            self.conn.commit()
        except mysql.connector.Error as err:
            print('\033[31m' + f'Ошибка при сохранении запроса: {err}' + '\033[0m')

    def get_top_queries(self, limit=10):
        if not self.cursor:
            return []
        query = '''
            SELECT keyword, genre, year, COUNT(*) as count
            FROM search_results
            GROUP BY keyword, genre, year
            ORDER BY count DESC
            LIMIT %s
        '''
        try:
            self.cursor.execute(query, (limit,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print('\033[31m' + f'Ошибка при получении топ-запросов: {err}' + '\033[0m')
            return []

    def format_query(self, row):
        parts = []
        if row.get('keyword'):
            parts.append(str(row['keyword']))
        if row.get('genre'):
            parts.append(str(row['genre']))
        if row.get('year'):
            parts.append(str(row['year']))
        return ' '.join(parts) if parts else '(пустой запрос)'

    def print_top_queries(self):
        top = self.get_top_queries()
        for row in top:
            query_str = self.format_query(row)
            print(f'{query_str} — {row["count"]} раз')

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


