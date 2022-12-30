from ._http import HTTPRequests, json_decoder
from .exceptions import NOT_REGISTERED, INVALID_INPUT

class Maker:
    def __init__(self, auth: str) -> None:
        self.auth = auth
        self.http = HTTPRequests()

    def makeDATA(self, method: str, data: dict) -> dict:
        data = {
            'api_version': '0',
            'auth': self.auth,
            'client': {
                'app_name': 'Main',
                'app_version': '3.0.9',
                'lang_code': 'fa',
                'package': 'app.rbmain.a',
                'platform': 'Android',
                'temp_code': '10',
            },
            'data': data,
            'method': 'method',
        }
        return data

    async def request(self, method: str, data: dict) -> dict:
        data = self.makeDATA(method=method, data=data)
        response = await self.http.post(json=data)
        read = await json_decoder(await response.aread())
        if 'ERROR_ACTION' or 'ERROR_GENERIC' in (read.get('status'),):
            status_det: str = read.get('status_det')
            if status_det == 'NOT_REGISTERED':
                raise NOT_REGISTERED('Your AUTH ID is not registered in the Rubika server, please make sure your AUTH is correct')
            elif status_det == 'INVALID_INPUT':
                raise INVALID_INPUT('The data sent to the Rubino server is wrong')
            raise Exception(status_det)
        else:
            return read.get('data')