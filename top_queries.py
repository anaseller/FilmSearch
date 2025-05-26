

import mysql.connector
import local_settings
from datetime import datetime

class TopQueries:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=local_settings.DB_HOST,
            user=local_settings.DB_USER,
            password=local_settings.DB_PASSWORD,
            database=local_settings.DB_DATABASE
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def log_query(self, keyword, genre, year):
        query = '''
            INSERT INTO search_results (keyword, genre, year, search_time)
            VALUES (%s, %s, %s, %s)
        '''
        now = datetime.now()
        self.cursor.execute(query, (keyword, genre, year, now))
        self.conn.commit()

    def get_top_queries(self, limit=10):
        query = '''
            SELECT keyword, genre, year, COUNT(*) as count
            FROM search_results
            GROUP BY keyword, genre, year
            ORDER BY count DESC
            LIMIT %s
        '''
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()

    def format_query(self, row):
        parts = []
        if row['keyword']:
            parts.append(str(row['keyword']))
        if row['genre']:
            parts.append(str(row['genre']))
        if row['year']:
            parts.append(str(row['year']))
        return ' '.join(parts) if parts else '(пустой запрос)'

    def print_top_queries(self):
        top = self.get_top_queries()
        for row in top:
            query_str = self.format_query(row)
            print(f'{query_str} — {row["count"]} раз')

    def close(self):
        self.cursor.close()
        self.conn.close()


