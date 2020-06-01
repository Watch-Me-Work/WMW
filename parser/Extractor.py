from requests import Session
from bs4 import BeautifulSoup
import justext

class Response:
    ''' Response defines the returned object for Extractor.
    It includes segmented parts of the extracted web document.
    '''
    
    def __init__(self):
        self._title = ""
        self._body = ""
        self._raw = ""

    def get(self, name):
        ''' public interface, return the requested section of 
        the response.
        '''
        switcher = {
            "title": self._title,
            "body": self._body,
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
    3. Work well with a wide range of websites.
    '''
    
    def __init__(self):
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


class ContentExtractor():
    ''' Implementation of Extractor interface
    '''
    def __init__(self):
        super().__init__()
        self._response = Response()

    def _httpRequest(self, url):
        sess = Session()
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = sess.request(method="GET", url=url, headers=headers)
        
        return res.text

    def extractFromURL(self, url):
        html = self._httpRequest(url)
        self.extractFromHTML(html)

        return self._response

    def extractFromHTML(self, html):
        soup = BeautifulSoup(html, "html.parser")
        self._response._title = soup.title.string

        text = ""
        ps = justext.justext(html, justext.get_stoplist("English"))
        for p in ps:
            if not p.is_boilerplate:
                text += p.text

        self._response._body = text
        self._response._raw = html
        return self._response


def main():
    # usage of example extractor
    url = "https://www.foxnews.com/politics/grenell-declassifies-names-of-obama-officials-who-unmasked-flynn-report-says"
    url = "https://github.com/dalab/web2text"
    url = "https://medium.com/@laura.derohan/compiling-c-files-with-gcc-step-by-step-8e78318052"
    url = "https://www.geeksforgeeks.org/tabulation-vs-memoization/"

    # sess = Session()
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # res = sess.request(method="GET", url=url, headers=headers)
    # html = res.text
    
    parser = ContentExtractor()
    # response = parser.extractFromHTML(html)
    response = parser.extractFromURL(url)
    print(response.get("body"))


if __name__ == '__main__':
    main()
