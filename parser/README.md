# Parser API
#### `ContentExtractor`

`extractCleanText(html="", url="")`

*Extracting clean text from given HTML and/or URL, return a response object*

Args:

- `html`: the target html to cleanup, this will be considered first if provided
- `url`: the target url to cleanup, if html is empty, or no html is provided, or html is corrupted, this url, if provided, will be used to extract clean text

Return:

* `Response` object





#### `Response`

`get(name)`

*Getting information from Response object by a provided name. Return specified information.*

Args:

* `name`: name of target segment, options includes:
    * `title`: document title
    * `body`: main body
    * `raw`: raw html string
    * `first`: first paragraph
    * `status`: parsing status, `True` if nothing goes wrong, `False` if something goes wrong
    * `error`: error message of parser, if `status` flag is `True`

Return:

* Strings of specified information.

