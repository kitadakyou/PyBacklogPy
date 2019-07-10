from requests import Response
from typing import Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Status:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'statuses'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_status_list(self) -> Response:
        """
        状態一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-status-list/

        :return: レスポンス
        """

        path = self.base_path
        return self.rs.send_get_request(path=path, url_param={})
