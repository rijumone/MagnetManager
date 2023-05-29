import requests
from loguru import logger
from bs4 import BeautifulSoup

MAIN_SEARCH_URL = 'https://piratesbay.tk/search.php?q=john+wick+4&cat=0'
MAIN_SEARCH_URL = 'https://piratebay.pro/get-data-for'

def perform_request(searchterm, category=0):
    # params = {
    #     'q': searchterm,
    #     'cat': category,
    # }
    # logger.debug(params)
    # return requests.get(MAIN_SEARCH_URL, params=params)
    url = f'{MAIN_SEARCH_URL}/{searchterm}'
    logger.debug(url)
    return requests.get(url)

def fetch_list(searchterm):
    '''
    1. Load "MAIN_SEARCH_URL" to bs4
    2. Return {
        "title": str,
        "uploaded": date,
        "magnet_uri": str,
        "size": str,
        "SE": int,
        "LE": int,
        "uploader": str,
    }
    '''
    raw_body = perform_request(searchterm)
    if raw_body.status_code != 200:
        raise ValueError(f'raw_body.status_code: {raw_body.status_code}')
    source = raw_body.content
    soup = BeautifulSoup(source, 'html5lib')
    table = soup.find('table', class_='table')
    rows = table.find_all('tr')
    _ctr = 0
    _lst = []
    for row in rows:
        _dct = {}
        if _ctr == 0:
            _ctr += 1
            continue # skip header
        
        # import pdb;pdb.set_trace()
        tds = row.find_all('td')
        _as = tds[0].find('a')
        
        _dct['title'] = _as.text

        _as = tds[2].find('a')
        _dct['magnet_uri'] = _as['href']
        _dct['uploaded'] = tds[1].find('span').text
        _dct['size'] = tds[3].find('span').text
        _dct['uploader'] = tds[4].find('a').text


            
            
        
        _lst.append(_dct)

    return _lst
    # import pdb;pdb.set_trace()

if __name__ == '__main__':
    _o = fetch_list(searchterm='john wick 4')
    print(_o)