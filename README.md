![](https://img.shields.io/badge/dynamic/json?color=success&label=Version&prefix=v&query=%24.version&url=https%3A%2F%2Fraw.githubusercontent.com%2Fwciesialka%2Fthe%2Fmaster%2Finfo.json) ![](https://img.shields.io/badge/dynamic/json?color=informational&label=Python&query=%24.python&url=https%3A%2F%2Fraw.githubusercontent.com%2Fwciesialka%2Fthe%2Fmaster%2Finfo.json)

# the
Generate an image of Barnacle Boy holding THE OBJECT

## Prerequisites

* Python 3.8+
* PIL
* A Google account
* A [Google Custom Search Engine](https://cse.google.com/cse/all)

The Python modules required can be installed using `pip install -r requirements.txt` if the pip module is installed. Details on how to install pip can be found [on their website](https://pip.pypa.io/en/stable/installing/).


## About Google Custom Search Engine

To use this program, you must have generated a [Google Custom Search Engine](https://cse.google.com/cse/all). The program will ask you to enter your CX and JSON API Key. Please follow the instructions and do not share these keys with anyone. You must have "Image Search" turned on. It is also recommended that you turn on "Search the entire web." You may want to read the details on the [Developer's Page](https://developers.google.com/custom-search/v1/overview).

## Using

Run from the command line using:

```
python main.py [options] query
options:
    -u, --update_key        Begin with a prompt to update your Google Custom Search API key and CX.
    -o, --output            Path to output file.
    -k, --key               Forces use of a provided Google Custom Search API key.
    -c, --cx                Forces use of a provided Google Custom Search CX.
    -p, --pipe              Output raw bytes of image in JPEG format to STDOUT.
```

Note that query is a string and may require you to surround it in quotations, especially if it contains spaces.

If no `--output` option is given, the file will be output with the pattern `out/the (query).jpg`, with `out` being created on the same level as `main.py` if not already existing. This will not happen if the `--pipe` flag is set.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Authors

* William Ciesialka