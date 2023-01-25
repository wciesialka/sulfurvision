'''Module responsible for making requests without exceeding a reasonable limit.'''

# This file is part of sulfurvision.
# sulfurvision is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software Foundation, 
# version 3 of the License. sulfurvision is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details. You should have received a copy of the GNU General Public License along with
# sulfurvision. If not, see <https://www.gnu.org/licenses/>.

from typing import Dict, Optional
from urllib.parse import urlencode, urlparse
from urllib.error import URLError
from time import sleep, perf_counter_ns
from contextlib import contextmanager
import urllib.request

class Requester:

    '''Class responsible for making requests.


    :ivar user_agent: User agent of the requests.
    :type user_agent: str
    '''

    def __init__(self, user_agent: str, request_delay_ms: int = 100):
        '''Constructor method.

        :param user_agent: User agent of the requests.
        :type user_agent: str
        :param request_delay_ms: Minimum time between requests in milliseconds.
        :type request_delay_ms: int
        '''
        # Private hosts dictionary used to keep track of requests.
        self.__hosts: Dict[str, int] = {}
        self.user_agent: str = user_agent
        # Multiply by 1_000_000 to convert ms -> ns
        self.__request_delay_ns = 1_000_000 * request_delay_ms

    @contextmanager
    def open(self, url: str, params: Optional[Dict[str, str]] = None):
        '''Open a GET request to a url with the given parameters.

        :param url: URL to send a GET request to.
        :type url: str
        :param params: Parameters for the GET request, defaults to None
        :type params: Dict[str, str], optional
        :raises ex: Raises a URLError if one should occur.
        :yield: Context Manager provided by urllib urlopen.
        '''
        host: str = urlparse(url).netloc

        # Check if the host is in the list of recent hosts, and wait if so.
        if host in self.__hosts:
            last_call = self.__hosts[host]
            time_diff = perf_counter_ns() - last_call

            if time_diff < self.__request_delay_ns:
                delay_ns = self.__request_delay_ns - time_diff
                # Must divide by 1e+9 to account for ns -> secs
                sleep(delay_ns / 1e+9)

        if params is not None:
            # Form URL with format url?params
            url = '?'.join((url, urlencode(params)))

        # Make the request
        request = urllib.request.Request(url)
        request.add_header('User-Agent', self.user_agent)
        try:
            response = urllib.request.urlopen(request)
            self.__hosts[host] = perf_counter_ns()
            yield response
        except URLError as ex:
            raise ex
        else:
            response.close()
