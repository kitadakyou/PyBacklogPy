from requests import Response
from typing import Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Licence:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_licence(self,
                    ) -> Response:
        """
        ライセンス情報の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-licence/


        :return: レスポンス
        """

        path = 'space/licence'

        return self.rs.send_get_request(path=path, url_param={})
