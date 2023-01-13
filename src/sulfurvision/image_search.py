'''Module responsible for searching for an image.'''

# This file is part of sulfurvision.
# sulfurvision is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software Foundation, 
# version 3 of the License. sulfurvision is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details. You should have received a copy of the GNU General Public License along with
# sulfurvision. If not, see <https://www.gnu.org/licenses/>.

import urllib.request
import re
import json
from urllib.parse import urlencode
from html import escape as htmlescape
from os import getenv
from typing import List
from PIL import Image

WHITESPACE_REGEX: re.Pattern = re.compile(r"\s+", re.MULTILINE)

class UnsuccessfulRequest(Exception):
    '''Exception representing an unsuccessful request.'''

    def __init__(self, status_code: int, response: str):
        super().__init__(f"Invalid request returned status code {status_code}.\
            Response:\n\t{response}")

def find_results(query: str, start: int = 1) -> List[str] | None:
    '''Function responsible for searching for and finding image URLs.

    :param query: Query string.
    :type query: str
    :param start: Pagination start, defaults to 1
    :type start: int, optional
    :raises TypeError: Query must be string
    :raises TypeError: Start must be int
    :raises ValueError: Start must be greater than or equal to one.
    :raises ValueError: Query must be less than or equal to 1840 characters in length.
    :raises QueryError: Query must not be empty.
    :raises UnsuccessfulRequest: Raises when a request is unsuccessful.
    :return: The images found, or None if no results found.
    :rtype: list[str] | None
    '''

    CS_KEY: str = getenv('GOOGLE_CS_KEY')
    CS_CX: str = getenv('GOOGLE_CS_CX')

    if not isinstance(query, str):
        try:
            query = str(query)
        except Exception:
            raise TypeError(
                f"query should be type 'str', not type '{query.__class__.__name__}'"
            )
    if not isinstance(start, int):
        raise TypeError(
            f"start should be type 'int', not type '{start.__class__.__name__}'"
        )
    if start < 1:
        raise ValueError(f"start should be >= 1, not {start}")
    query = query.strip()
    query = htmlescape(query)
    query = WHITESPACE_REGEX.sub("+", query)

    if len(query) > 1840:
        # 1840 is the approximately the length a query can be before the 
        # complete request url is over 2000 characters
        raise ValueError(
            "Query must be less than or equal to 1840 characters in length."
        )
    elif len(query) == 0:
        raise ValueError('Query should not be empty.')
    else:
        params = urlencode(
            {'key': CS_KEY, "cx": CS_CX, "q": query,
            "searchType": 'image', "start": start}
        )
        url = f"https://www.googleapis.com/customsearch/v1?{params}"
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'sulphurvision/2.0')
        with urllib.request.urlopen(request) as response:
            if response.getcode() == 200:
                data = json.load(response)
                return data.get('items', None)
            else:
                raise UnsuccessfulRequest(response.getcode(), str(response.read()))

MAX_SEARCHES: int = 5
RESULTS_PER_SEARCH: int = 10

def search(query: str) -> Image.Image | None:
    '''Find the first available image URL and return an Image containing it.

    :param query: Query to search for
    :type query: str
    :return: The first available image, or None if none were found.
    :rtype: Image.Image | None
    '''
    image = None
    i = 0
    while image is None and i < MAX_SEARCHES:
        n = (i * RESULTS_PER_SEARCH) + 1
        results = find_results(query, start = n)
        for result in results: # loop through results and try to find a valid one
            try:
                url = result.get('link')
                request = urllib.request.Request(url)
                request.add_header('User-Agent', 'sulphurvision/2.0')
                with urllib.request.urlopen(request) as response:
                    image = Image.open(response)
            except Exception:
                continue
            else:
                break
        i += 1
        if len(results) < n + 10:
            break

    return image
