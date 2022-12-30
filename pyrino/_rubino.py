from ._make import Maker
from typing import Optional

class Client:
    def __init__(self, auth: str) -> None:
        self.make = Maker(auth)

    async def getMyProfileInfo(self, profile_id: Optional[str] = None) -> dict:
        '''Method: getMyProfileInfo

This method is used to get user account information in Rubino
If you want to get the information of your home page, you don't need the profile_id parameter, otherwise, enter the profile_id of your page!

Example:
    app.getMyProfileInfo()
    or
    app.getMyProfileInfo('profile_id')'''

        if profile_id is not None:
            data = {'profile_id': profile_id}
        else:
            data = {}
        return await self.make.request(
            method='getMyProfileInfo',
            data=data,
        )