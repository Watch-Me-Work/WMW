from requests import Session
from requests import exceptions
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
        self._status = True
        self._error = ""

    def get(self, name):
        ''' public interface, return the requested section of 
        the response.
        '''
        switcher = {
            "title": self._title,
            "body": self._body,
            "raw": self._raw,
            "first": self._first,
            "status": self._status,
            "error": self._error
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
        
        return res.text, res.status_code

    def extractCleanText(self, html="", url=""):
        if not html and not url:
            self._response._status = False
            self._response._error = "InputError: HTML and URL are both empty."
            return self._response

        if not html:
            try:
                html, status_code = self._httpRequest(url)
                if status_code != 200:
                    self._response._status = False
                    self._response._error = "HTTPError: " + str(status_code)
                    return self._response
            except requests.exceptions.Timeout:
                self._response._status = False
                self._response._error = "RequestError: Timeout."
                return self._response
            except requests.exceptions.TooManyRedirects:
                self._response._status = False
                self._response._error = "RequestError: TooManyRedirects."
                return self._response
            except requests.exceptions.RequestException as e:
                self._response._status = False
                self._response._error = "RequestError: RequestException."
                return self._response
            except:
                self._response._status = False
                self._response._error = "RequestError: Error."
                return self._response

        try:
            soup = BeautifulSoup(html, "html.parser")
        except:
            self._response._status = False
            self._response._error = "BS4Error: Parsing failed."
            return self._response
        if soup.title is not None:
            self._response._title = soup.title.string

        text = ""
        first = False
        try:
            ps = justext.justext(html, justext.get_stoplist("English"))
        except:
            self._response._status = False
            self._response._error = "JusTextError: Parsing failed."
            return self._response

        for p in ps:
            if not p.is_boilerplate:
                text += p.text
                if first == False and len(p.text.split(" "))>5:
                    self._response._first = p.text
                    first = True
        
        self._response._body = text
        self._response._raw = html

        return self._response
# TODO: if html fails, use url

def main():
    # usage of example extractor
    parser = ContentExtractor()
    url = "https://www.geeksforgeeks.org/tabulation-vs-memoization/"

    # test by passing only url
    # res = parser.extractCleanText(url=url)

    # test by passing html and url
    html = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    <p class="story">...</p>
    """
    res = parser.extractCleanText(html=html, url=url)

    # sess = Session()
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # res = sess.request(method="GET", url=url, headers=headers)
    # html = res.text
    
    # print results
    print(res.get("body"))
    print("############################################")
    print(res.get("title"))
    print("############################################")
    print(res.get("first"))
    print("############################################")
    print(res.get("status"))
    print("############################################")
    print(res.get("error"))
    print("############################################")


if __name__ == '__main__':
    main()
