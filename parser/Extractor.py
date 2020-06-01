from requests import Session
from bs4 import BeautifulSoup
import justext
from html2text import HTML2Text

class Response:
    ''' Response defines the returned object for Extractor.
    It includes segmented parts of the extracted web document.
    '''
    
    def __init__(self):
        self._title = ""
        self._body = ""
        self._raw = ""
        self._first = ""

    def get(self, name):
        ''' public interface, return the requested section of 
        the response.
        '''
        switcher = {
            "title": self._title,
            "body": self._body,
            "raw": self._raw,
            "first": self._first
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
        status, html = self._requestPage(url)
        text = self._htmlToText(html)
        self._response = Response()
        self._response._body = text
        return self._response

    def extractFromHTML(self, html):
        text = self._htmlToText(html)
        self._response = Response()
        self._response._body = text
        return self._response



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
        if soup.title is not None:
            self._response._title = soup.title.string

        text = ""
        first = False
        ps = justext.justext(html, justext.get_stoplist("English"))
        for p in ps:
            if not p.is_boilerplate:
                text += p.text
                if first == False and len(p.text.split(" "))>5:
                    self._response._first = p.text
                    first = True
        self._response._body = text
        self._response._raw = html
        return self._response
    





def main():
    # usage of example extractor
    url = "https://www.foxnews.com/politics/grenell-declassifies-names-of-obama-officials-who-unmasked-flynn-report-says"
    url = "https://github.com/dalab/web2text"
    url = "https://medium.com/@laura.derohan/compiling-c-files-with-gcc-step-by-step-8e78318052"
    url = "https://www.geeksforgeeks.org/tabulation-vs-memoization/"
    url = "https://www.cnn.com/2020/05/26/media/trump-joe-scarborough-conspiracy-theory/index.html"

    # sess = Session()
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # res = sess.request(method="GET", url=url, headers=headers)
    # html = res.text
    
    parser = ContentExtractor()
    # response = parser.extractFromHTML(html)
    response = parser.extractFromURL(url)
    print(response.get("first"))


if __name__ == '__main__':
    main()
