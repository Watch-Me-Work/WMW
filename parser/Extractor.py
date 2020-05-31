from requests import Session
from html2text import HTML2Text
from bs4 import BeautifulSoup
from parser import obtain_content

class Response:
    ''' Response defines the returned object for Extractor.
    It includes segmented parts of the extracted web document.
    '''
    
    def __init__(self):
        self._header = ""
        self._body = ""
        self._footer = ""
        self._text = ""
        self._raw = ""

    def get(self, name):
        ''' public interface, return the requested section of 
        the response.
        '''
        switcher = {
            "header": self._header,
            "body": self._body,
            "footer": self._footer,
            "text": self._text,
            "raw": self._raw
        }
        return switcher[name]


class Extractor:
    ''' Extractor Interface is used to extract clean text from web 
    documents. It returns a Response object, which could be used by 
    search module to further extract keywords and search against 
    given corpus.
    Intented implementations:
    1. Supports both static and dynamic web documents.
    2. Produces text with minimal noise.
    3. Work well with most web pages.
    '''
    
    def __init__(self):
        ''' Initialize Response object
        '''
        self._response = Response()
        pass

    def extractFromURL(self, url):
        ''' Public interface for extracting clean text from url
        '''
        pass

    def extractFromHTML(self, html):
        ''' Public interface for extracting text from given html string
        '''
        pass


class H2TExtractor(Extractor):
    ''' Example html2text implementation of Extractor
    '''

    def __init__(self):
        super().__init__()

    def _requestPage(self, url):
        sess = Session()
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = sess.request(method="GET", url=url, headers=headers)
        return res.status_code, res.text

    def _htmlToText(self, html):
        text_maker = HTML2Text()
        text = text_maker.handle(html)
        return text

    def extractFromURL(self, url):
        if "docs.google.com" in url:
            status, html = self._requestPage(url)
            text = obtain_content(url)
            self._response._text = text
        else:
            status, html = self._requestPage(url)
            text = self._htmlToText(html)
            self._response._text = text
        return self._response

    def extractFromHTML(self, html):
        text = self._htmlToText(html)
        self._response._text = text
        return self._response


class BS4Extractor(Extractor):
    """docstring for BS4Extractor"""
    def __init__(self):
        super().__init__()

    def _requestPage(self, url):
        sess = Session()
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = sess.request(method="GET", url=url, headers=headers)
        return res.status_code, res.text

    def _texttobs4(self, text):
        soup = BeautifulSoup(text,"html.parser")
        body = soup.find("body")
        p = body.find_all("p",text=True)
        text = ""
        for node in p:
            text += str(node.find_all(text=True))
        return text

    def extractFromURL(self, url):
        status, html = self._requestPage(url)
        text = self._texttobs4(html)
        self._response._text = text
        return self._response

    def extractFromHTML(self, html):
        text = self._texttobs4(html)
        self._response._text = text
        return self._response


def main():
    # usage of example extractor
    url = "https://www.foxnews.com/politics/grenell-declassifies-names-of-obama-officials-who-unmasked-flynn-report-says"

    sess = Session()
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = sess.request(method="GET", url=url, headers=headers)
    
    extractor = BS4Extractor()
    res = extractor.extractFromHTML(res.text)
    print(res.get("text"))


if __name__ == '__main__':
    main()
