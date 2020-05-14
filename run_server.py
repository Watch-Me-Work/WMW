from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

from search import BingRelatedDocumentFinder, DummyRelatedDocumentFinder, CorpusRelatedDocumentFinder
from parser import Response, H2TExtractor

HOSTNAME = 'localhost'
WMW_PORT = 3380

class WmwRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(self.path)
        request_params = json.loads(self.rfile.read(int(self.headers['content-length'])).decode('utf-8'))
        finder = CorpusRelatedDocumentFinder()
        extractor = H2TExtractor()
        # TODO: This does not conform to API.  Should be extract(), not _htmlToText(), but can't be fixed until parser conforms to API.
        text = extractor._htmlToText(request_params['document_html'])
        tmp = Response()
        tmp._text = text
        result = finder.search(tmp)
        result = {'results': [{'title': r.get_title()} for r in result]}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

if __name__ == "__main__":
    print(f"Starting server on host={HOSTNAME}, port={WMW_PORT}")
    server = HTTPServer((HOSTNAME, WMW_PORT), WmwRequestHandler)

    server.serve_forever()

