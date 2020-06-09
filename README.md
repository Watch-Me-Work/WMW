# WMW
Watch Me Work: A Chrome Extension for Real-time Automatic Searching

## Getting started

To install the Chrome extension, open Chrome and go to `chrome://extensions`.  Enable Developer Mode in the top right corner and then click 'Load extension' and browse to the `ui/extension_bundle` folder in this repository.

The server needs to be running in order for the browser extension to work.  There are two ways to set up the server application.  The first and simplest is to go to the [releases](https://github.com/Watch-Me-Work/WMW/releases) page and download the appropriate exectuable for your operating system.  Then you can just run that file.

### Source code install
The second way is to install from the source code.  This assumes you already have Python installed.  Make sure you are using Python 3.6 or higher and your current directory is set to the root of this repository.  Do `pip install -r requirements.txt` to install dependencies.  Then run `python init.py` to download and setup data (if you prefer manually doing this for some reason, see 'Manual download of data' below').

To start the server, run:
```
python3 run_server.py
```

#### Manual download of data
Instead of using `init.py` you may download data manually.  Download https://northwestern.box.com/shared/static/iu3hhk9msqng57ac93vlf7ns2acqi8h1.zip and extract it in the `search/` directory.  If done successfully, you should now have a `middata/` folder inside the `search/` directory.  You'll also need the "wordnet" package installed for NLTK, which can be done by running `python3 -c 'import nltk; nltk.download("wordnet");`.

## Bing search engine
By default, the extension only searches Wikipedia articles.  To use Bing as the backend for search, start the server with the `--finder_type bing` option.  You will also need to export the `BING_KEY` environment variable with the Bing API key.  This key is listed in the WatchMeWork Slack (if you aren't part of the watch me work team, you can obtain a [free trial key](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/) on the Bing API website.


## Building a standalone release

To build a standalone executable that runs the server, you can use pyinstaller.  Install with `pip install pyinstaller` and then do `pyinstaller --onefile run_server.spec` to build the executable (which will be in the `dist/` folder when pyinstaller finishes).
