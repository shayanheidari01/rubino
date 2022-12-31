from .._make import Maker
from random import randint

class Posts:
    def __init__(self, maker: Maker) -> None:
        self.Make = maker

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
        data = {
            'caption': caption,
            'file_id': file_id,
            'hash_file_receive': hash_file_receive,
            'height': height,
            'is_multi_file': is_multi_file,
            'post_type': post_type,
            'rnd': await self.rnd(),
            'thumbnail_file_id': thumbnail_file_id,
            'thumbnail_hash_file_receive': thumbnail_hash_file_receive,
            'width': width,
            'profile_id': profile_id,
        }
        return await self.make.request(
            method='addPost',
            data=data,
        )

    async def rnd(self) -> int:
        return randint(100000000, 999999999)