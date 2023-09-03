import os
import urllib
from pprint import pprint
import requests
from loguru import logger

from stem.control import Controller
from stem import Signal
from selenium import webdriver
from bs4 import BeautifulSoup


class CloudBackend:
    def __init__(self) -> None:
        # self.set_new_tor_session()
        pass

    def set_new_tor_session(self, ):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(os.getenv('TOR_CONTROLLER_PASSWORD'))
            controller.signal(Signal.NEWNYM)
        session = requests.session()
        # Tor uses the 9050 port as the default socks port
        session.proxies = {'http':  'socks5://127.0.0.1:9050',
                           'https': 'socks5://127.0.0.1:9050'}
        self.session = session

    def load_url_tor_selenium(self, searchterm, ):
        search_url = f'https://yts.rs/browse-movies/{urllib.parse.quote(searchterm)}/all/all/0/latest'
        logger.debug(search_url)
        # response = self.session.get(search_url)
        # print(response.text)
        options = webdriver.firefox.options.Options()

        options.set_preference('network.proxy.type', 1)
        options.set_preference('network.proxy.socks', '127.0.0.1')
        options.set_preference('network.proxy.socks_port', 9050)
        options.set_preference('network.proxy.socks_remote_dns', False)

        driver = webdriver.Firefox(options=options)
        driver.get('http://icanhazip.com')
        try:
            driver.get(search_url)
        finally:
            driver.quit()

    def search(self, searchterm):
        search_url = f'https://en.yify.uno/movies?keyword={searchterm}'
        response = requests.get(search_url)
        return response.text

    def parse_html(self, raw_html):
        # print(raw_html)
        results_soup = BeautifulSoup(raw_html, features="html.parser")
        html_results = results_soup.select(
            'body > div.main-content > div.browse-content > div > section > div > div:nth-child(n)')
        # import pdb;pdb.set_trace()
        for h_r in html_results:
            img_src = None
            img = h_r.find('img')
            link_html = h_r.select('a.browse-movie-title')[0]
            if img:
                img_src = img.get('data-src', None)
            _dct = {
                # 'id': link.split('/')[-1],
                'title': link_html.text,
                'url': link_html['href'],
                'img': img_src,
                'year': h_r.select('div.browse-movie-year')[0].text,
                'rating': h_r.select('h4.rating')[0].text,
                'genre': h_r.select('h4')[1].text,
            }
            yield _dct

    def get_magnet(self, url):
        response = requests.get(url)
        return response.text

    def parse_html_magnets(self, raw_html):

        magnets_soup = BeautifulSoup(raw_html, features="html.parser")
        html_magnets = magnets_soup.select(
            '#movie-info > p:nth-child(2) > a:nth-child(n)')
        for magnet in html_magnets:
            _dct = {
                'quality': magnet.text,
                'magnet_link': magnet['href'],
            }
            yield _dct


def search(searchterm):
    '''Search for search term in available backends'''
    cb = CloudBackend()
    results = cb.parse_html(cb.search(searchterm))
    for _r in results:
        yield _r


def get_magnet(url):
    '''Get magnet links for passed url'''
    cb = CloudBackend()
    results = cb.parse_html_magnets(cb.get_magnet(url))
    for _r in results:
        yield _r


if __name__ == '__main__':
    # searchterm = 'john wick'
    # results = search(searchterm)
    url = 'https://en.yify.uno/movies/john-wick-chapter-4-2023-imdb600'
    results = get_magnet(url)
    pprint(list(results))
