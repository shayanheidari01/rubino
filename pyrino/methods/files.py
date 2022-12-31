from .._make import Maker

class Files:
    def __init__(self, maker: Maker) -> None:
        self.make = maker

    async def requestUploadFile(self, file_name: str, file_size: int, file_type: str, profile_id: str) -> dict:
        '''
        method: requestUploadFile

        This method is to send the upload request to the Rubika's server for uploading, it is actually a prerequisite for uploading!
        If we do not send this request before uploading the file to the server, we will not be able to upload a file due to insufficient information.

        Example:
            app.requestUploadFile(file_name='file.png', file_size=500, file_type='Picture', profile_id='...')
        '''

        if type(file_size) != int:
            file_size = int(file_size)

        data = {
            'file_name': file_name,
            'file_size': file_size,
            'file_type': file_type,
            'profile_id': profile_id,
        }

        return await self.make.request(
            method='requestUploadFile',
            data=data,
        )

    async def uploadFile(self, upload_url: str, file: bytes, hash_file_request: str, file_id: str) -> str:
        return await self.make.uploadFile(
            upload_url=upload_url,
            file=file,
            hash_file_request=hash_file_request,
            file_id=file_id,
        )