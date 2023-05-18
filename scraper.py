import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup


def __main__():
    URLS = [
        'https://nomanssky.fandom.com/wiki/Gek_(language)',
        'https://nomanssky.fandom.com/wiki/Korvax_(language)',
        'https://nomanssky.fandom.com/wiki/Vy%27keen_(language)'
    ]

    for url in URLS:
        print(f'Processing {url}...')

        # Get the language name from the URL
        language = unquote(url).split('/')[-1].split('_')[0]
        print(f'Language: {language}')

        # Get the HTML from the URL
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Get the table from the HTML
        table = soup.select('table.wikitable')[0]
        table_body = table.find('tbody')

        # Get the rows from the table
        rows = table_body.find_all('tr')

        # Get the words from the rows
        file = open(f'dict/{language}.txt', 'w')

        file.write(str(len(rows) - 1) + '\n')

        for row in rows[1:]:
            columns = row.find_all('td')

            english = columns[0].text
            foreign = columns[1].text
            foreign_caps = columns[2].text
            foreign_all_caps = columns[3].text

            if english != '':
                file.write(
                    f'{english}: {foreign};{foreign_caps};{foreign_all_caps}')


if __name__ == '__main__':
    __main__()
