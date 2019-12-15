from requests import Response
from typing import List, Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Status:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects/'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def add_status(self,
                   project_id_or_key: str,
                   name: str,
                   color: str,
                   ) -> Response:
        """
        権限メソッドURLURL パラメーターリクエストパラメーターレスポンス例
        https://developer.nulab.com/ja/docs/backlog/api/2/add-status/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param name: 状態の名前
        :param color: 状態の背景色；以下から指定”#ea2c00””#e87758””#e07b9a””#868cb7””#3b9dbd””#4caf93””#b0be3c””#eda62a””#f42858””#393939”

        :return: レスポンス
        """

        path = self.base_path + project_id_or_key + '/statuses'
        payloads = {'name': name, 'color': color}
        return self.rs.send_post_request(path=path, request_param=payloads)

    def update_status(self,
                      project_id_or_key: str = None,
                      status_id: int = None,
                      name: str = None,
                      color: str = None,
                      ) -> Response:
        """
        権限メソッドURLURL パラメーターリクエストパラメーターレスポンス例
        https://developer.nulab.com/ja/docs/backlog/api/2/update-status/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param status_id: 状態のID
        :param name: 状態の名前
        :param color: 状態の背景色；以下から指定”#ea2c00””#e87758””#e07b9a””#868cb7””#3b9dbd””#4caf93””#b0be3c””#eda62a””#f42858””#393939”

        :return: レスポンス
        """

        path = self.base_path + '{project_id_or_key}/statuses/{status_id}'\
            .format(project_id_or_key=project_id_or_key, status_id=status_id)
        payloads = {}
        if name:
            payloads['name'] = name
        if color:
            payloads['color'] = color
        return self.rs.send_patch_request(path=path, request_param=payloads)

    def delete_status(self,
                      project_id_or_key: str,
                      status_id: int,
                      substitute_status_id: int,
                      ) -> Response:
        """
        権限メソッドURLURL パラメーターリクエストパラメーターレスポンス例
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-status/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param status_id: 状態のID
        :param substitute_status_id: 紐づく課題を付け替える先の状態のID。削除対象の状態が設定されている課題がある場合、このパラメーターで指定した状態へ一括変更します。

        :return: レスポンス
        """

        path = self.base_path + '{project_id_or_key}/statuses/{status_id}' \
            .format(project_id_or_key=project_id_or_key, status_id=status_id)
        payloads = {'substituteStatusId': substitute_status_id}
        return self.rs.send_delete_request(path=path, request_param=payloads)

    def update_order_of_status(self,
                               project_id_or_key: str,
                               status_id: List[int],
                               ) -> Response:
        """
        権限メソッドURLURL パラメーターリクエストパラメーターレスポンス例
        https://developer.nulab.com/ja/docs/backlog/api/2/update-order-of-status/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param status_id: 表示順に並べた、状態のIDのリスト。そのプロジェクトで使える全ての状態を渡してください。表示順には以下の制限があります未対応は先頭にあること完了は末尾にあること処理中は処理済みよりも前にあること

        :return: レスポンス
        """

        path = self.base_path + '{project_id_or_key}/statuses/updateDisplayOrder'\
            .format(project_id_or_key=project_id_or_key)
        payloads = {'statusId[]': status_id}
        return self.rs.send_patch_request(path=path, request_param=payloads)
