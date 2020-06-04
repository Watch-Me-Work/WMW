from requests import Session
from requests import exceptions
from bs4 import BeautifulSoup
import justext
from html2text import HTML2Text
from .drive_extractor import obtain_content

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

    def extractCleanText(self, html="", url=""):
        ''' Public interface for extracting clean text from given
        html and url, default to use html first
        '''
        pass


# class H2TExtractor(Extractor):
#     ''' Example html2text implementation of Extractor
#     '''

#     def __init__(self):
#         super().__init__()

#     def _requestPage(self, url):
#         sess = Session()
#         headers = {'User-Agent': 'Mozilla/5.0'}
#         res = sess.request(method="GET", url=url, headers=headers)
#         return res.status_code, res.text

#     def _htmlToText(self, html):
#         text_maker = HTML2Text()
#         text = text_maker.handle(html)
#         return text

#     def extractFromURL(self, url):
#         status, html = self._requestPage(url)
#         text = self._htmlToText(html)
#         self._response = Response()
#         self._response._body = text
#         return self._response

#     def extractFromHTML(self, html):
#         text = self._htmlToText(html)
#         self._response = Response()
#         self._response._body = text
#         return self._response


class ContentExtractor(Extractor):
    ''' Implementation of Extractor interface
    '''
    def __init__(self):
        super().__init__()
        self._response = Response()

    def _httpRequest(self, url):
        try:
            sess = Session()
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = sess.request(method="GET", url=url, headers=headers)
            html = res.text
            status_code = res.status_code
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

        return html, status_code

    def _extract(self, html):
        # extract title
        title = ""
        try:
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.string
        except:
            title = ""

        # extract body and first paragraph
        body = ""
        first = ""
        isFirst = False
        ps = justext.justext(html, justext.get_stoplist("English"))

        end_punctuation = ['.','?','!']
        for p in ps:
            if not p.is_boilerplate:
                body += p.text
                if isFirst == False:
                    p_count = 0
                    for ep in end_punctuation:
                        p_count += p.text.count(ep)
                    if len(p.text.split(" "))>20 or p_count > 2:
                        first = p.text
                        isFirst = True


        return title, body, first

    def extractCleanText(self, html="", url=""):
        # if both inputs are empty
        if not html and not url:
            self._response._status = False
            self._response._error = "InputError: HTML and URL are both empty."
            return self._response

        if "docs.google.com" in url:
            html, status_code = self._httpRequest(url)
            body = obtain_content(url)
            self._response._title = ""
            self._response._body = body
            self._response._first = body
            self._response._raw = html

        else:
            
            # use url or html
            use_url = False

            # if html is empty, use url
            if not html:
                html, status_code = self._httpRequest(url)
                use_url = True

            # extract title, body, first paragraph
            try:
                title, body, first = self._extract(html)
            except:
                self._response._status = False
                self._response._error = "ExtractError: Extract failed."
                return self._response

            # if using html did not get anything, use url
            if not title and not body and not first and not use_url:
                html, status_code = self._httpRequest(url)
                use_url = True
                try:
                    title, body, first = self._extract(html)
                except:
                    self._response._status = False
                    self._response._error = "ExtractError: Extract failed."
                    return self._response

            self._response._title = title
            self._response._body = body
            self._response._first = first
            self._response._raw = html

        return self._response


def main():
    # usage of example extractor
    parser = ContentExtractor()
    url = "https://docs.google.com/document/d/1QeVDSu1ZNWHHB3qg6FLcodmwe51yWQKabASRc0iepSg/edit"

    # test by passing only url
    res = parser.extractCleanText(url=url)

    # test by passing html and url
    # html = """
    # <html><head><title>The Dormouse's story</title></head>
    # <body>
    # <p class="title"><b>The Dormouse's story</b></p>
    # <p class="story">Once upon a time there were three little sisters; and their names were
    # <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    # <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    # <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    # and they lived at the bottom of a well.</p>
    # <p class="story">...</p>
    # """
    # res = parser.extractCleanText(html=html, url=url)

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
