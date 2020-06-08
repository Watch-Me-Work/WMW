import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s -   %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

import search
from search import NerRelatedDocumentFinder, TopicRelatedDocumentFinder
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
        extractor = self.server.text_extractor
        logger.info('Running parser pipeline for {}'.format(request_params['url']))
        doc_content = extractor.extractCleanText(html=request_params['document_html'], url=request_params['url'])
        logger.info('Running search pipeline for {}'.format(request_params['url']))
        result = self.server.topic_finder.search(doc_content, max_results=2)
        results_list = [
            {
                'title': r.get_title(),
                'url': r.get_url(),
                'snippet': r.get_snippet(),
                'source': 'topic',
            }
            for r in result]

        result = self.server.ner_finder.search(doc_content, max_results=3)
        results_list.extend([
            {
                'title': r.get_title(),
                'url': r.get_url(),
                'snippet': r.get_snippet(),
                'source': 'ner',
            }
            for r in result])

        result = {'results': results_list}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

class WmwServer(HTTPServer):
    def __init__(self, cmdargs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmdargs = cmdargs

        if self.cmdargs.parser_type == 'justext':
            self.text_extractor = ContentExtractor()
        else:
            raise ValueError("Unknown parser type")

        engine = None
        if self.cmdargs.finder_type == 'bing':
            engine = search.BingSearchEngine()
        elif self.cmdargs.finder_type == 'wiki':
            engine = search.WikipediaSearchEngine()
        elif self.cmdargs.finder_type == 'corpus':
            engine = search.CorpusSearchEngine()
        self.ner_finder = NerRelatedDocumentFinder(engine)
        self.topic_finder = TopicRelatedDocumentFinder(engine)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--parser_type', choices=['justext'], default='justext')
    parser.add_argument('--finder_type', choices=['bing', 'corpus', 'wiki'], default='wiki')
    args = parser.parse_args()

    print(f"Starting server on host={HOSTNAME}, port={WMW_PORT}")
    server = WmwServer(cmdargs=args, server_address=(HOSTNAME, WMW_PORT), RequestHandlerClass=WmwRequestHandler)

    server.serve_forever()

