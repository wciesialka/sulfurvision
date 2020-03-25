import html, re, requests

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
            raise TypeError(f"query should be type str, not {type(query)}")
        if not isinstance(start,int):
            raise TypeError(f"start should be type int, not {type(start)}")
        if start < 1:
            raise ValueError(f"start should be >= 1, not {start}")
        q = query.strip()
        q = html.escape(q)
        q = ImageSearch.WHITESPACE_REGEX.sub("+",q)

        params = {'key': self.key, "cx": self.cx, "q": q, "searchType": 'image', start: start}
        r = requests.get(url=ImageSearch.URL,params=params)

        data = r.json()

        return data['items']