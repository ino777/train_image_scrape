import logging
import yaml

from mylib.image_scraper import fetch_image_urls, save_img, make_file_path
from opencv.opencv import make_train_img, make_train_path
from config import get_keyword


# What images you try to scrape
# WARNING: if IMG_KEYWORD is Japanese language, it'd cause error
IMG_KEYWORD = get_keyword('Img Keyword')


def main():
    logging.info('start')
    image_urls = fetch_image_urls(IMG_KEYWORD, 25)
    for i, url in enumerate(image_urls):
        file_path = make_file_path(IMG_KEYWORD, i)
        save_img(url, file_path)

        make_train_img(file_path, make_train_path(IMG_KEYWORD, i))
    logging.info('end')


if __name__ == "__main__":
    formatter = '%(levelname)s %(name)s: %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)

    main()
