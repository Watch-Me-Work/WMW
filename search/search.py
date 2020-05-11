import os
import requests

class FoundDocument:
    def __init__(self, title):
        self.title = title

    def get_title(self):
        return self.title


class BingSearchEngine:
    def __init__(self):
        self._subscription_key = os.environ['BING_KEY']
        self._endpoint = 'https://watchmework.cognitiveservices.azure.com/bing/v7.0/search'

    def search_by_string(self, query_string):
        params = { 'q': query_string, 'mkt': 'en-US' }
        headers = { 'Ocp-Apim-Subscription-Key': self._subscription_key }

        try:
            response = requests.get(self._endpoint, headers=headers, params=params)
            response.raise_for_status()
            found_documents = []
            for result in response.json()['webPages']['value']:
                found_documents.append(FoundDocument(result['name']))
            return found_documents
        except Exception as ex:
            raise ex

class DummySearchEngine:
    def __init__(self):
        pass

    def search_by_string(self, query_string):
        titles_const = ['Southern Hemisphere - Wikipedia', 'The Differences Between Northern & Southern Hemisphere ...', 'Geography of the Southern Hemisphere and Facts', 'Which Countries Are in the Southern Hemisphere ...', 'Countries Located Completely in the Southern Hemisphere ...', "A Beginner's Guide to the Southern Hemisphere Sky - Sky ...", 'Are we prepared for COVID-19 hitting the southern hemisphere?', 'Southern Hemisphere | Definition of Southern Hemisphere by ...', 'Southern hemisphere | Definition of Southern hemisphere at ...', 'Southern Constellations – Constellation Guide'] 
        return [FoundDocument(title) for title in titles_const]
