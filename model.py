from werkzeug.contrib.cache import SimpleCache

from bs4 import BeautifulSoup

import urllib
import re
from datetime import datetime
from unicodedata import normalize


cache = SimpleCache(['127.0.0.1:11211'])

def clean_text(text):
    return normalize('NFKD', text.decode('latin-1')).encode('ASCII', 'ignore')


class RU(object):

    def get_menu(self):
        menu = cache.get('uece_ru_menu')
        if menu is None:
            menu = self._update_menu()
            cache.set('uece_ru_menu', menu, timeout=60 * 60 * 6)
        return menu

    def _update_menu(self):
        try:
            html_doc = urllib.urlopen('http://www.uece.br/uece/index.php/ru/2379')
        except IOError:
            return {'error': 'Bad gateway'}
        soup = BeautifulSoup(html_doc)
        ru_trs = soup.find_all('tr', 'ru_head_title')
        json_as_python = []
        for tr in ru_trs:
            date = tr.text.strip().encode('latin-1')
            date = clean_text(date)
            date_match = re.match(r'\S+ - \(?(?P<day>\d{2}/\d{2})(/\d{2,4})?\)?', date)
            if date_match:
                date = date_match.groupdict()
                year = str(datetime.now().year)
                day, month = date['day'].split('/')
                date['day'] = '%s-%s-%s' % (year, month, day)
            else:
                date = {'day': date}
            content = tr.find_next('tr').find('td').text.strip()
            content = re.sub(r'[Ss]ob[\.:]\s?', 'Sobremesa: ', content)
            content = content.encode('utf-8')
            content = content.split('\n')[:-1]
            json_as_python.append({
                'date': date['day'],
                'menu': content
            })
        return json_as_python


if __name__ == '__main__':
    ru = RU()
    print ru.get_menu()
