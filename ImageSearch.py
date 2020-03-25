import html, re, requests

class ImageSearch:

    WHITESPACE_REGEX = re.compile(r"\s+",re.MULTILINE)
    URL = r"https://www.googleapis.com/customsearch/v1"

    def __init__(self,key:str, cx:str):
        if not isinstance(key,str):
            raise TypeError(f"key should be type str, not {type(key)}")
        elif not isinstance(cx,str):
            raise TypeError(f"cx should be type str, not {type(cx)}")
        else:
            self.key = key
            self.cx = cx

    def search(self,query):
        q = query.strip()
        q = html.escape(q)
        q = ImageSearch.WHITESPACE_REGEX.sub("+",q)

        params = {'key': self.key, "cx": self.cx, "q": q, "searchType": 'image', 'safe': 'off'}
        r = requests.get(url=ImageSearch.URL,params=params)

        data = r.json()

        return data['items']