import html, re, requests

class UnsuccessfulRequest(Exception):
    def __init__(self,status_code:int):
        self.status_code = status_code
        self.message = f"Invalid request: returned status code {self.status_code}"
    
    def __str__(self):
        return self.message

class QueryError(Exception):
    def __init__(self,description):
        self.description = description
        self.message = self.description
        
    def __str__(self):
        return self.message

class ImageSearch:

    WHITESPACE_REGEX = re.compile(r"\s+",re.MULTILINE)
    URL = r"https://www.googleapis.com/customsearch/v1"

    def __init__(self,key:str, cx:str):
        if not isinstance(key,str):
            raise TypeError(f"key should be type str, not {type(key)}")
        if not isinstance(cx,str):
            raise TypeError(f"cx should be type str, not {type(cx)}")
        self.key = key
        self.cx = cx

    def search(self,query:str,start:int):
        if not isinstance(query,str):
            try:
                query = str(query)
            except:
                raise TypeError(f"query should be type str, not {type(query)}")
        if not isinstance(start,int):
            raise TypeError(f"start should be type int, not {type(start)}")
        if start < 1:
            raise ValueError(f"start should be >= 1, not {start}")
        q = query.strip()
        q = html.escape(q)
        q = ImageSearch.WHITESPACE_REGEX.sub("+",q)

        if len(q) > 1840: # 1840 is roughly the length a query can be before the total request url is over 2000 characters
            raise ValueError("Query must be less than or equal to 1840 characters in length.")
        elif q == "":
            raise QueryError('Query should not be empty.')
        else:
            params = {'key': self.key, "cx": self.cx, "q": q, "searchType": 'image', "start": start}
            r = requests.get(url=ImageSearch.URL,params=params)
            if r.status_code == 200:
                data = r.json()

                return data['items']
            else:
                raise UnsuccessfulRequest(r.status_code)