

from search_module import SearchModule
from top_queries import TopQueries
import math

def main():
    searcher = SearchModule()
    logger = TopQueries()

    while True:
        print('\n--- Меню ---')
        print('''Эта программа позволяет искать фильмы по базе данных Sakila. 
Поиск можно выполнить по ключевому слову, жанру, году выпуска. Искать можно по одному или сразу нескольким параметрам.''')
        print('1. Поиск фильмов по параметрам')
        print('2. Топ 10 самых популярных запросов')
        print('0. Выход')

        choice = input('Выберите опцию: ')
        if choice == '1':
            genres = searcher.get_genres()
            print('\nВыберите жанр из списка или нажмите 0, чтобы пропустить выбор жанра:')
            for idx, genre_name in enumerate(genres, 1):
                print(f'{idx}. {genre_name}')
            genre_choice = input('Введите номер жанра (или 0 для пропуска): ')
            genre = genres[int(genre_choice) - 1] if genre_choice.isdigit() and int(genre_choice) > 0 and int(genre_choice) <= len(genres) else None

            keyword = input('Введите ключевое слово (или Enter чтобы пропустить): ')
            year = input('Введите год (или Enter чтобы пропустить): ')
            year = int(year) if year else None

            results = searcher.combined_search(keyword or None, genre, year)
            logger.log_query(keyword or None, genre, year)

            total = len(results)
            if total == 0:
                print('\nНет результатов по заданным критериям.')
                continue

            results_per_page = 15
            pages = math.ceil(total / results_per_page)
            current_page = 1

            while True:
                start = (current_page - 1) * results_per_page
                end = start + results_per_page
                print(f'\n--- Результаты (страница {current_page}/{pages}) ---')
                for title, release_year, description, category in results[start:end]:
                    print(f'{title} ({release_year}) - {category}\n{description}\n')

                if pages == 1:
                    break

                print('1 — следующая страница, 0 — выход в главное меню')
                print(f'\n--- Результаты (страница {current_page}/{pages}) ---')
                nav = input('> ').strip().lower()
                if nav == '1' and current_page < pages:
                    current_page += 1
                elif nav == '0':
                    break
                else:
                    print('Неверный ввод.')

        elif choice == '2':
            print('\n--- Топ 10 самых популярных запросов ---')
            logger.print_top_queries()

        elif choice == '0':
            break
        else:
            print('Неверный ввод. Попробуйте снова.')

    searcher.close()
    logger.close()

if __name__ == '__main__':
    main()

