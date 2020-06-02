# WMW
Watch Me Work: A Chrome Extension for Real-time Automatic Searching

## Getting started

First, make sure you are using Python 3.6 or higher and do `pip install -r requirements.txt` to install dependencies.  To start the server, run:
```
python3 run_server.py
```

To install the Chrome extension, open Chrome and go to `chrome://extensions`.  Enable Developer Mode in the top right corner and then click 'Load extension' and browse to the `ui/extension_bundle` folder in this repository.

## Bing search engine
To use Bing as the backend for search, start the server with the `--finder_type bing` option.  You will also need to export the `BING_KEY` environment variable with the Bing API key.  This key is listed in the WatchMeWork Slack.
