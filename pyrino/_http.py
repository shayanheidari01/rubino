from httpcore import AsyncConnectionPool, Response, RemoteProtocolError
from json import JSONEncoder, JSONDecoder
from typing import Optional
from random import randint

org_headers: dict = {
    'Content-Type': 'application/json; charset=UTF-8',
    'User-Agent': 'okhttp/3.12.1',
}
decoder = JSONDecoder()

async def makeURL(url) -> bytes:
    if type(url) == bytes:
        return url
    else:
        return url.encode('UTF-8')

async def makeRubinoURL() -> bytes:
    dc: int = randint(a=1, b=10)
    return f'https://rubino{dc}.iranlms.ir/'.encode('UTF-8')

async def json_decoder(json) -> dict:
    if type(json) == bytes:
        json = json.decode('UTF-8')
    return decoder.decode(s=json)

class HTTPRequests:
    def __init__(self) -> None:
        self.http = AsyncConnectionPool(http2=True)
        self.encoder = JSONEncoder()

    async def get(self, url: bytes, headers: Optional[dict] = None) -> Response:
        while 1:
            try:
                url: makeURL = await makeURL(url=url)
                response = await self.http.request(b'GET', url, headers=headers)
                return response
            except RemoteProtocolError:
                self.http = AsyncConnectionPool(http2=True)

    async def post(self,
        url: Optional[bytes] = None,
        data: Optional[bytes] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> Response:
        if url is None:
            url = await makeRubinoURL()

        if json is not None:
            data = self.encoder.encode(o=json).encode('UTF-8')

        while 1:
            try:
                url: makeURL = await makeURL(url=url)
                response = await self.http.request(b'POST', url=url, content=data, headers=org_headers)
                return response
            except RemoteProtocolError:
                self.http = AsyncConnectionPool(http2=True)