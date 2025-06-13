# Das ist die Hauptseite der Anwendung,
# hier befindet sich die gesamte Anwendungslogik, hauptsächlich mein Teil,
# die Eingabe von Befehlen durch den Benutzer.

from search_module import SearchModule
from top_queries import TopQueries

def main():
    searcher = SearchModule()
    logger = TopQueries()

    print('\033[94m' + '''\nWelcome!
This program lets you search for films in the Sakila database.
You can search by keyword, genre, or release year — individually or in combination.''' + '\033[0m')

    while True:
        print('\033[96m' + '\n====== MENU ======' + '\033[0m')
        print('1. Search films by parameters')
        print('2. Top 10 most popular queries')
        print('0. Exit')

        choice = input('\033[96m' + 'Select an option: ' + '\033[0m').strip()
        if choice == '1':
            genres = searcher.get_genres()
            print('\nChoose a genre from the list or press 0 to skip:')
            for idx, genre_name in enumerate(genres, 1):
                print(f'{idx}. {genre_name}')

            while True:
                genre_choice = input('\033[96m' + 'Enter the genre number (or 0 to skip): ' + '\033[0m').strip()
                if genre_choice.isdigit():
                    genre_num = int(genre_choice)
                    if 0 <= genre_num <= len(genres):
                        break
                print('\033[31m' + 'Invalid input. Please try again.' + '\033[0m')

            genre = genres[genre_num - 1] if genre_num != 0 else None

            # genre_choice = input('\033[96m' + 'Введите номер жанра (или 0 для пропуска): ' + '\033[0m').strip()
            # genre = genres[int(genre_choice) - 1] if genre_choice.isdigit() and int(genre_choice) > 0 and int(genre_choice) <= len(genres) else None

            keyword = input('\033[96m' + 'Enter a keyword (or press Enter to skip): ' + '\033[0m').strip()
            year = input('\033[96m' + 'Enter the year (or press Enter to skip): ' + '\033[0m').strip()
            year = int(year) if year.isdigit() else None

            results = searcher.combined_search(keyword or None, genre, year)
            logger.log_query(keyword or None, genre, year)

            total = len(results)
            if total == 0:
                print('\033[31m' + '\nNo results found for the given criteria.' + '\033[0m')
                continue

            results_per_page = 15
            pages = (total + results_per_page - 1) // results_per_page
            current_page = 1

            while True:
                start = (current_page - 1) * results_per_page
                end = start + results_per_page
                print(f'\n--- Results (page {current_page}/{pages}) ---')
                for title, release_year, description, category in results[start:end]:
                    print(f'{title} ({release_year}) - {category}\n{description}\n')

                if pages == 1:
                    break

                print('1 — next page, 0 — return to main menu')
                print(f'--- Results (page {current_page}/{pages}) ---')

                while True:
                    nav = input('> ').strip()
                    if nav == '1' and current_page < pages:
                        current_page += 1
                        break
                    elif nav == '0':
                        break
                    else:
                        print('\033[31m' + 'Invalid command. Please try again.' + '\033[0m')
                if nav == '0':
                    break

        elif choice == '2':
            print('\n--- Top 10 most popular searches ---')
            logger.print_top_queries()

        elif choice == '0':
            break
        else:
            print('\033[31m' + 'Invalid input. Please try again.' + '\033[0m')

    searcher.close()
    logger.close()

if __name__ == '__main__':
    main()