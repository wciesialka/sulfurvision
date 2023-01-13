'''Module responsible for making requests without exceeding a reasonable limit.'''

# This file is part of sulfurvision.
# sulfurvision is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software Foundation, 
# version 3 of the License. sulfurvision is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details. You should have received a copy of the GNU General Public License along with
# sulfurvision. If not, see <https://www.gnu.org/licenses/>.

from typing import Dict
from urllib.parse import urlencode, urlparse
from time import sleep, perf_counter_ns
from contextlib import contextmanager
import urllib.request

class Requester:

    # Request Delay in Milliseconds
    REQUEST_DELAY_MS: int = 100
    # Request Delay in Nanoseconds
    REQUEST_DELAY: int = 1_000_000 * REQUEST_DELAY_MS

    def __init__(self, user_agent: str):
        self.__hosts: Dict[str, int] = {}
        self.user_agent = user_agent

    @contextmanager
    def open(self, url: str, params: Dict[str, str] | None = None):
        current_time = perf_counter_ns()
        host = urlparse(url).netloc
        if host in self.__hosts:
            last_call = self.__hosts[host]
            time_diff = current_time - last_call
            if time_diff < Requester.REQUEST_DELAY:
                delay_ns = Requester.REQUEST_DELAY - time_diff
                # Must divide by 1e+9 to account for ns -> secs
                sleep(delay_ns / 1e+9)
        
        if params is not None:
            url = '?'.join((url, urlencode(params)))

        request = urllib.request.Request(url)
        request.add_header('User-Agent', self.user_agent)
        try:
            response = urllib.request.urlopen(request)
            self.__hosts[host] = current_time
            yield response
        except Exception as ex:
            raise ex
        else:
            self.__hosts[host] = current_time
        finally:
            response.close()