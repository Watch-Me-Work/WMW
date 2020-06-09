import tarfile
import tempfile

import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s -   %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

import urllib.request
import zipfile
import nltk


if __name__ == '__main__':
    logger.info('Installing NLTK data...')
    nltk.download('wordnet')

    logger.info('Downloading topic model resources...')
    urllib.request.urlretrieve('https://northwestern.box.com/shared/static/iu3hhk9msqng57ac93vlf7ns2acqi8h1.zip', filename='search/middata.zip')
    with zipfile.ZipFile('search/middata.zip') as zf:
        zf.extractall(path='search/')

