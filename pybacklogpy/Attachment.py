from requests import Response
from typing import Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Attachment:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'space'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def post_attachment_file(self,
                             filepath: str,
                             filename: str) -> Response:
        """
        添付ファイルの送信
        https://developer.nulab.com/ja/docs/backlog/api/2/post-attachment-file/

        :param filepath: 添付ファイルのパス
        :param filename: 任意のファイル名

        :return: レスポンス
        """

        path = self.base_path + '/attachment'
        files = {'file': (filename, open(filepath, 'rb'))}
        return self.rs.post_file(path=path, files=files)
