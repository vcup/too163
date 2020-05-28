import re
import urllib3


class data_download:

    def __init__(self, headers: dict = None):
        self.http = urllib3.PoolManager(headers=headers)

    def type_handan(self) -> dict:
        content_type = self.req.headers.get('content-type')  # like 'text/plain;charset=UTF-8'
        content_type = re.split(';|; ', content_type)
        data_type = content_type[0]
        data_charset = content_type[1][8:]
        return {'type': data_type, 'charset': data_charset}

    def __truediv__(self, url):
        self.req = self.http.request('get', url)
        return self.type_handan()

    __rtruediv__ = __truediv__
    set = __init__
    set_req = __truediv__
