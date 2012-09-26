import urllib
from bs4 import BeautifulSoup
import re

class RU(object):

    def get_menu(self):
        html_doc = urllib.urlopen('http://www.uece.br/uece/index.php/ru/2379')
        soup = BeautifulSoup(html_doc)
        ru_trs = soup.find_all('tr', 'ru_head_title')
        json_as_python = {}
        for tr in ru_trs:
            day = tr.text.strip().encode('latin-1')
            content = tr.find_next('tr').find('td').text.strip()
            content = re.sub(r'[Ss]ob[\.:]\s?', 'Sobremesa: ', content)
            content = content.encode('latin-1')
            content = content.split('\n')[:-1]
            json_as_python[day] = content
        return json_as_python
