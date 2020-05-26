import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

from search import BingRelatedDocumentFinder, DummyRelatedDocumentFinder, CorpusRelatedDocumentFinder
from parser import Response, ContentExtractor

HOSTNAME = 'localhost'
WMW_PORT = 3380

class WmwRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/find_related':
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'unknown endpoint'}).encode('utf-8'))
            return

        request_params = json.loads(self.rfile.read(int(self.headers['content-length'])).decode('utf-8'))
        finder = self.server.doc_finder
        extractor = self.server.text_extractor
        doc_content = extractor.extractFromHTML(request_params['document_html'])
        result = finder.search(doc_content)
        result = {'results': [{'title': r.get_title()} for r in result]}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

class WmwServer(HTTPServer):
    def __init__(self, cmdargs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmdargs = cmdargs

        if self.cmdargs.parser_type == 'h2t':
            self.text_extractor = H2TExtractor()
        elif self.cmdargs.parser_type == 'bs4':
            self.text_extractor = BS4Extractor()
        elif self.cmdargs.parser_type == 'justext':
            self.text_extractor = ContentExtractor()
        else:
            raise ValueError("Unknown parser type")

        if self.cmdargs.finder_type == 'bing':
            self.doc_finder = BingRelatedDocumentFinder()
        elif self.cmdargs.finder_type == 'corpus':
            self.doc_finder = CorpusRelatedDocumentFinder()
        else:
            raise ValueError("Unknown finder type")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--parser_type', choices=['justext'], default='justext')
    parser.add_argument('--finder_type', choices=['bing', 'corpus'], default='corpus')
    args = parser.parse_args()

    print(f"Starting server on host={HOSTNAME}, port={WMW_PORT}")
    server = WmwServer(cmdargs=args, server_address=(HOSTNAME, WMW_PORT), RequestHandlerClass=WmwRequestHandler)

    server.serve_forever()

