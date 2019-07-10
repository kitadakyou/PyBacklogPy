from requests import Response
from typing import Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Resolution:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'resolutions'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_resolution_list(self) -> Response:
        """
        完了理由一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-resolution-list/

        :return: レスポンス
        """

        path = self.base_path
        return self.rs.send_get_request(path=path, url_param={})
