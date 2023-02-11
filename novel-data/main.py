
import re

import requests

from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator


class RequestBase:
    def __init__(self, url: str):
        self.url = url

    def page_source(self) -> BeautifulSoup:
        source = requests.get(self.url)
        return BeautifulSoup(source.text, 'html.parser')

    def later_calls(self, url_page) -> BeautifulSoup:
        source = requests.get(url_page)
        return BeautifulSoup(source.text, 'html.parser')


class NovelChapterLinks(RequestBase):
    def __int__(self, novel_url: str):
        super().__init__(novel_url)

    def pages_links_of_chapters(self) -> list:
        last_pagination_number = self.page_source().find(class_='last').a.get('data-page')
        # +2 é is used because the range takes one less numb,
        # and the las_pagination_number already comes with another one less
        all_possible_page_numbers = range(1, int(last_pagination_number) + 2)
        return [self.url + str(i) for i in all_possible_page_numbers]

    def get_chapter_links(self) -> list:
        try:
            chapter_links = []
            for link_pagination in self.pages_links_of_chapters():
                for links in self.later_calls(link_pagination).find_all(class_='list-chapter'):
                    for link in links.find_all('a'):
                        chapter_links.append(link.get('href'))

            return chapter_links
        except AttributeError:
            print('An error happened')
            self.get_chapter_links()


full_url = 'https://novelfull.com/pursuit-of-the-truth.html?page='


class NovelChapter(RequestBase):
    def __int__(self, chapter_url: str):
        super().__init__(chapter_url)

    def _get_chapter_content(self) -> list:
        soup = self.page_source()
        return soup.find(id='chapter-content').findAll('p')

    def translate_chapter_content(self):
        translated_text = []
        for i in self._get_chapter_content():
            print(i)
            translated_text.append(GoogleTranslator('en', 'pt').translate(text=str(i)))
        return translated_text

    def save_chapter_content(self):
        chapter_translated = self.translate_chapter_content()
        # chapter_translated = self._get_chapter_content()
        html = f'''
            <!DOCTYPE html>
            <html lang="pt-br">
              <head>
                <title>{str(chapter_translated[1])}</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
              </head>
              <body>
                {"".join([str(i) for i in chapter_translated])}
              </body>
            </html>
            '''
        number_chapter = re.findall(r'\d+', str(chapter_translated[1]))[0]
        with open(f'chapters/{number_chapter}.html', 'w') as f:
            f.write(str(html))


URL = 'https://novelfull.com'
url_part_name_novel = '/pursuit-of-the-truth/chapter-633-bright-yangs-mystery.html'
full_url = 'https://novelfull.com/pursuit-of-the-truth.html?page=1'
url_format = f'{URL}{url_part_name_novel}'

if __name__ == '__main__':
    novel_chapters_links = NovelChapterLinks(full_url).get_chapter_links()
    print(novel_chapters_links)
    for url_page in novel_chapters_links[:10]:
        NovelChapter(URL + url_page).save_chapter_content()
