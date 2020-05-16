# Parser API
####`BS4Extractor()`

`extractFromURL(url)`

*Extracting clean text from given URL, return a response object*

Args:

- `url`: the target url to cleanup

Return:

* `Response` object



`extractFromHTML(html)`

*Extracting clean text from given html string, return a response object.*

Args:

* `html`: string representation of a HTML file to cleanup

Return:

* `Response` object





#### `Response()`

`get(name)`

*Getting parsed segments of the input document. Return string representations.*

Args:

* `name`: name of target segment, options including "header", "body", "footer", "text", "raw"

Return:

* Strings of specified part of the document.