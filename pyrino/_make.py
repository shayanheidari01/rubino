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
            'method': method,
        }
        return data

    def makeUploadHeaders(self, hash_file_request: str, file_id: str) -> dict:
        headers = {
            'auth': self.auth,
            'hash-file-request': hash_file_request,
            'file-id': file_id,
            'Content-Type': 'application/octet-stream',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.1',
        }
        return headers

    async def request(self, method: str, data: dict) -> dict:
        data = self.makeDATA(method=method, data=data)
        response = await self.http.post(json=data)
        read = await json_decoder(await response.aread())
        #print(read)
        if (read.get('status') == 'ERROR_ACTION') or (
            read.get('status') == 'ERROR_GENERIC'
        ):
            status_det: str = read.get('status_det')
            if status_det == 'NOT_REGISTERED':
                raise NOT_REGISTERED('Your AUTH ID is not registered in the Rubika server, please make sure your AUTH is correct')
            elif status_det == 'INVALID_INPUT':
                raise INVALID_INPUT('The data sent to the Rubino server is wrong')
            raise Exception(status_det, read)
        else:
            return read.get('data')

    async def uploadFile(self, upload_url: str, file: bytes, hash_file_request: str, file_id: str) -> str:
        headers = self.makeUploadHeaders(
            hash_file_request=hash_file_request,
            file_id=file_id,
        )
        size = len(file)

        if size <= 131072:
            headers['part-number'] = '1'
            headers['total-part'] = '1'
            response = await self.http.postData(
                url=upload_url,
                data=file,
                headers=headers,
            )
            read = await json_decoder(await response.aread())
            assert read.get('status') == 'OK'
            return read.get('data').get('hash_file_receive')

        else:
            total_part = size // 131072 + 1
            for part_number in range(1, total_part + 1):
                bsb = (part_number - 1) * 131072 # base set file bytes
                headers['chunk-size'] = '131072' if part_number != total_part else str(len(file[bsb:]))
                headers['part-number'] = str(part_number)
                headers['total-part'] = str(total_part)

                if part_number != total_part:
                    data = file[bsb:bsb + 131072]
                    response = await self.http.postData(
                        url=upload_url,
                        data=data,
                        headers=headers,
                    )
                    read = await json_decoder(await response.aread())
                    assert read.get('status') == 'OK'
                    continue

                else:
                    response = await self.http.postData(
                        url=upload_url,
                        data=file[bsb:],
                        headers=headers,
                    )
                    read = await json_decoder(await response.aread())
                    assert read.get('status') == 'OK'
                    return read.get('data').get('hash_file_receive')