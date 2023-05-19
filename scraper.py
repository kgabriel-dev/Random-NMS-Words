import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup, ResultSet
import os


def __main__():
    URLS = [
        'https://nomanssky.fandom.com/wiki/Gek_(language)',
        'https://nomanssky.fandom.com/wiki/Korvax_(language)',
        'https://nomanssky.fandom.com/wiki/Vy%27keen_(language)',
        'https://nomanssky.fandom.com/wiki/Atlas_(language)'
    ]

    for url in URLS:
        print(f'Processing {url}...')

        # Get the language name from the URL
        language = unquote(url).split('/')[-1].split('_')[0]
        print(f'Language: {language}')

        # Get the HTML from the URL
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        tables = soup.select('table.wikitable')
        print(f'Tables found: {len(tables)}')

        data = None

        for table in tables:
            table_rows = table.findAll('tr')[1:]

            # Get the rows from the table
            if data:
                data.extend(table_rows)
            else:
                data = table_rows

        # Store the rows in a file
        storeRows(data if data else [], language)


def storeRows(rows, filename):
    # check if the directory exists
    try:
        os.mkdir('dict')
    except FileExistsError:
        pass

    # Create the file
    file = open(os.path.join('dict', f'{filename}.txt'), 'w')

    # write a placeholder with 3 symbols to be replaced later by 3 digits
    file.write('###\n')
    total_words = 0

    for row in rows:
        columns = row.find_all('td')

        if len(columns) == 4:
            english = columns[0].get_text(strip=True)
            foreign = columns[1].get_text(strip=True)
            foreign_caps = columns[2].get_text(strip=True)
            foreign_all_caps = columns[3].get_text(strip=True)
        elif len(columns) == 3:
            english = columns[0].get_text(strip=True)
            foreign = columns[1].get_text(strip=True)
            foreign_caps = columns[2].get_text(strip=True)
            foreign_all_caps = ''
        else:
            english = ''
            foreign = ''
            foreign_caps = ''
            foreign_all_caps = ''

        if english != '':
            file.write(f'{english}:{foreign};{foreign_caps};{foreign_all_caps}\n')
            total_words += 1

    file.seek(0)
    file.write(f'{total_words:03d}')

    file.close()


if __name__ == '__main__':
    __main__()
