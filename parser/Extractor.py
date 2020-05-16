from requests import Session
from html2text import HTML2Text
from bs4 import BeautifulSoup
import justext


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
    
    def __init__(self, extractor):
        ''' Initialize Response object
        '''
        pass

    def extractFromURL(self, url):
        ''' Public interface for extracting clean text from url
        '''
        pass

    def extractFromHTML(self, html):
        ''' Public interface for extracting text from given html string
        '''
        pass


class ContentExtractor(Extractor):
    ''' Implementation of Extractor interface
    '''
    def __init__(self, extractor):
        super().__init__(extractor)
        self._extractor = extractor
        self._response = Response()

    def _httpRequest(self, url):
        sess = Session()
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = sess.request(method="GET", url=url, headers=headers)
        
        return res.text

    def _bs4Extractor(self, html):
        soup = BeautifulSoup(html, "html.parser")
        body = soup.find("body")
        p = body.find_all("p", text=True)
        text = ""
        for node in p:
            text += str(node.find_all(text=True))
        
        return text

    def _justextExtractor(self, html):
        ps = justext.justext(html, justext.get_stoplist("English"))
        text = ""
        for p in ps:
            if not p.is_boilerplate:
                text += p.text

        return text

    def extractFromURL(self, url):
        html = self._httpRequest(url)
        self.extractFromHTML(html)

        return self._response

    def extractFromHTML(self, html):
        text = ""
        if self._extractor == "justext":
            text = self._justextExtractor(html)
        elif self._extractor == "bs4":
            text = self._bs4Extractor(html)
        else:
            raise Exception("Invalid extractor name")

        self._response._body = text
        return self._response


def main():
    # usage of example extractor
    url = "https://www.foxnews.com/politics/grenell-declassifies-names-of-obama-officials-who-unmasked-flynn-report-says"

    sess = Session()
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = sess.request(method="GET", url=url, headers=headers)
    html = res.text
    
    parser = ContentExtractor("bs4")
    response = parser.extractFromHTML(html)
    print(response.get("body"))


if __name__ == '__main__':
    main()
