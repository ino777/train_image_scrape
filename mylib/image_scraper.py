"""
Image scraper from google images according to config.yml 'img_keyword'
"""
import os
import re
import logging
import yaml
from PIL import Image
import urllib



from bs4 import BeautifulSoup
import requests


logger = logging.getLogger(__name__)


def fetch_image_urls(keyword, limit=100):
    """
    Return image urls fetched from google images site according to keyword

    limit:
        max number of scraping image urls
    """
    logger.info({
        'action': 'fetch_images',
        'keyword': keyword,
        'limit': limit,
        'status': 'run'
    })
    if not keyword:
        raise TypeError('Keyword must not be \'NoneType\'')
    elif not type(keyword) == str:
        raise TypeError('Keyword must be string')
    
    # image list
    payload = {'tbm': 'isch', 'q': urllib.parse.quote(keyword), 'source': 'lnms'}
    payload_str = '&'.join('%s=%s' % (k, v) for k,v in payload.items())
    url = 'https://www.google.com/search' + '?' + payload_str
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    html = urllib.request.urlopen(urllib.request.Request(url, headers=header))
    soup = BeautifulSoup(html, 'html.parser')
    target_tags = soup.find_all('div', attrs={'class': 'rg_meta'}, limit=limit)

    if not target_tags:
        logger.warning({
            'action': 'fetch_images',
            'url': url,
            'status': 'Images not founded'
        })
        return None

    img_urls = []
    for tag in target_tags:
        m = (re.findall(
            r'(?<=\"ou\":\").*?(?=\")', str(tag)))

        if not m:
            continue
        img_urls.append(m[0])

    logger.info({
        'action': 'fetch_images',
        'image_urls': img_urls,
        'status': 'success'
    })

    return img_urls


def make_file_path(keyword, index):
    """ Return file name ('images/images/<keyword>/<keyword>_<index>') """
    new_images_path = 'images/images/{}'.format(keyword)
    os.makedirs(new_images_path, exist_ok=True)
    return '{0}/{1}_{2}.jpg'.format(new_images_path, keyword, index)


def save_img(url, file_path):
    logger.info({
        'action': 'save_img',
        'url': url,
        'file_name': file_path,
        'status': 'run'
    })
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        if os.path.exists(file_path):
            logger.info({
                'action': 'save_img',
                'message': '{} already exists and is overwritten'.format(file_path),
            })
        with open(file_path, 'wb') as f:
            f.write(r.content)
            logger.info({
                'action': 'save_img',
                'status': 'success'
            })

    else:
        logger.error({
            'action': 'save_img',
            'url': url,
            'file_name': file_path,
            'response_status_code': r.status_code,
            'status': 'fail'
        })