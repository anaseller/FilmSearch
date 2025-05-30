

from search_module import SearchModule
from top_queries import TopQueries

def main():
    searcher = SearchModule()
    logger = TopQueries()

    print('\033[94m' + '''\nДобро пожаловать!
Эта программа позволяет искать фильмы по базе данных Sakila.
Поиск можно выполнить по ключевому слову, жанру, году выпуска. Искать можно по одному или сразу нескольким параметрам.''' + '\033[0m')

    while True:
        print('\033[96m' + '\n====== МЕНЮ ======' + '\033[0m')
        print('1. Поиск фильмов по параметрам')
        print('2. Топ 10 самых популярных запросов')
        print('0. Выход')

        choice = input('\033[96m' + 'Выберите опцию: ' + '\033[0m').strip()
        if choice == '1':
            genres = searcher.get_genres()
            print('\nВыберите жанр из списка или нажмите 0, чтобы пропустить выбор жанра:')
            for idx, genre_name in enumerate(genres, 1):
                print(f'{idx}. {genre_name}')

            while True:
                genre_choice = input('\033[96m' + 'Введите номер жанра (или 0 для пропуска): ' + '\033[0m').strip()
                if genre_choice.isdigit():
                    genre_num = int(genre_choice)
                    if 0 <= genre_num <= len(genres):
                        break
                print('\033[31m' + 'Неверный ввод. Повторите попытку.' + '\033[0m')

            genre = genres[genre_num - 1] if genre_num != 0 else None

            # genre_choice = input('\033[96m' + 'Введите номер жанра (или 0 для пропуска): ' + '\033[0m').strip()
            # genre = genres[int(genre_choice) - 1] if genre_choice.isdigit() and int(genre_choice) > 0 and int(genre_choice) <= len(genres) else None

            keyword = input('\033[96m' + 'Введите ключевое слово (или Enter чтобы пропустить): ' + '\033[0m').strip()
            year = input('\033[96m' + 'Введите год (или Enter чтобы пропустить): ' + '\033[0m').strip()
            year = int(year) if year.isdigit() else None

            results = searcher.combined_search(keyword or None, genre, year)
            logger.log_query(keyword or None, genre, year)

            total = len(results)
            if total == 0:
                print('\033[31m' + '\nНет результатов по заданным критериям.' + '\033[0m')
                continue

            results_per_page = 15
            pages = (total + results_per_page - 1) // results_per_page
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
                print(f'--- Результаты (страница {current_page}/{pages}) ---')

                while True:
                    nav = input('> ').strip()
                    if nav == '1' and current_page < pages:
                        current_page += 1
                        break
                    elif nav == '0':
                        break
                    else:
                        print('\033[31m' + 'Неверная команда. Повторите ввод.' + '\033[0m')
                if nav == '0':
                    break

        elif choice == '2':
            print('\n--- Топ 10 самых популярных запросов ---')
            logger.print_top_queries()

        elif choice == '0':
            break
        else:
            print('\033[31m' + 'Неверный ввод. Попробуйте снова.' + '\033[0m')

    searcher.close()
    logger.close()

if __name__ == '__main__':
    main()