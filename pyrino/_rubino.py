from ._make import Maker
from .methods import users, files, posts
from typing import Optional

class Client:
    def __init__(self, auth: str) -> None:
        self.make = Maker(auth)
        self.Users = users.Users(maker=self.make)
        self.Files = files.Files(maker=self.make)
        self.Posts = posts.Posts(maker=self.make)

    async def getMyProfileInfo(self, profile_id: Optional[str] = None) -> dict:
        return await self.Users.getMyProfileInfo(profile_id=profile_id)

    async def requestUploadFile(self, file_name: str, file_size: int, file_type: str, profile_id: str) -> dict:
        return await self.Files.requestUploadFile(
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
            profile_id=profile_id,
        )

    async def uploadFile(self, upload_url: str, file: bytes, hash_file_request: str, file_id: str) -> str:
        return await self.Files.uploadFile(
            upload_url=upload_url,
            file=file,
            hash_file_request=hash_file_request,
            file_id=file_id,
        )
    
    async def addPost(self,
        post_type: str,
        profile_id: str,
        file_id: str,
        hash_file_receive: str,
        thumbnail_hash_file_receive: str,
        thumbnail_file_id: str,
        is_multi_file=False,
        height='200',
        width='200',
        caption=None
    ):
        return await self.Posts.addPost(
            post_type,
            profile_id,
            file_id,
            hash_file_receive,
            thumbnail_hash_file_receive,
            thumbnail_file_id,
            is_multi_file,
            height,
            width,
            caption,
        )