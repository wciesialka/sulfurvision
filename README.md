# Sulfur Vision
Generate an image of Barnacle Boy using sulfur vision on a held object. This object will be automatically obtained from Google Image results.

## Getting Started

### Installation

The recommended way to install the most up-to-date version of this project is by cloning the respository and running `python3 -m pip install -e .` in the repository directory. This allows you to control which branch you install as well. This may not always guarantee a stable release, however. Note that this requires the `pip` module, which should come with your installation of Python. If you do not have `pip`, details on how to install `pip` can be found [on their website](https://pip.pypa.io/en/stable/installation/). More in-depth details on how to install packages can be found [in the Python documentation](https://packaging.python.org/en/latest/tutorials/installing-packages/).

### Prerequisites

* Python 3.11.1+
* A Google account
* A [Google Custom Search Engine](https://cse.google.com/cse/all)

Dependencies are listed in [requirements.txt](requirements.txt) and should be automatically installed during setup. If this fails, you can install dependencies using `python3 -m pip install -r requirements.txt` if the `pip` module is installed. 

#### About Google Custom Search Engine

To use this program, you must have generated a [Google Custom Search Engine](https://cse.google.com/cse/all). You must have "Image Search" turned on. It is also recommended that you turn on "Search the entire web." You may want to read the details on the [Developer's Page](https://developers.google.com/custom-search/v1/overview).

### Setup

Before using this tool, you must set two environment variables. 

* `GOOGLE_CS_CX` should be set to your Search Engine ID.
* `GOOGLE_CS_KEY` should be set to your Custom Search JSON API Key.

For more details, visit [Custom Search JSON API: Introduction](https://developers.google.com/custom-search/v1/introduction).

## Usage

### Running the Program

After installation, you can run the program from the command line like so:

```
usage: sulfurvision [-h] [-o OUTPUT] query

Generate a Sulfur Vision image.

positional arguments:
  query                 Search query.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file.
```

Note that query is a string and may require you to surround it in quotations, especially if it contains spaces.

## Examples

You can view a pre-generated example at [examples/lenna.jpg](examples/lenna.jpg).
![Example Output](examples/lenna.jpg)

## License

This project is licensed under the The GNU General Public License v3.0 - see [LICENSE](LICENSE) for details.

## Authors

* Willow Ciesialka
