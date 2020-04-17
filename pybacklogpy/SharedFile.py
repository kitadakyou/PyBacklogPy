from requests import Response
from typing import Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class SharedFile:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_list_of_shared_files(self,
                                 project_id_or_key: str,
                                 file_path: str,
                                 order: str = 'desc',
                                 offset: Optional[int] = None,
                                 count: int = 1000,
                                 ) -> Response:
        """
        共有ファイル一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-shared-files/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param file_path: ディレクトリのパス
        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param offset:
        :param count: 取得上限(1-1000)  指定が無い場合は1000

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/files/metadata/{file_path}'\
            .format(project_id_or_key=project_id_or_key, file_path=file_path)
        payloads = {}
        if order is not None:
            if order not in {'desc', 'asc'}:
                raise ValueError('order は desc または asc のみが使用できます')
            payloads['order'] = order
        if offset is not None:
            payloads['offset'] = offset
        if count is not None:
            if not 1 <= count <= 1000:
                raise ValueError('count(取得上限)は1-1000の範囲で指定してください')

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_file(self,
                 project_id_or_key: Optional[str] = None,
                 shared_file_id: Optional[int] = None,
                 ) -> Response:
        """
        共有ファイルのダウンロード
        https://developer.nulab.com/ja/docs/backlog/api/2/get-file/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param shared_file_id: 共有ファイルのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/files/{shared_file_id}'\
            .format(project_id_or_key=project_id_or_key, shared_file_id=shared_file_id)

        return self.rs.send_get_request(path=path, url_param={})
