from requests import Response
from typing import Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Category:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_category_list(self,
                          project_id_or_key: str,
                          ) -> Response:
        """
        カテゴリー一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-category-list/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/categories'.format(project_id_or_key=project_id_or_key)

        return self.rs.send_get_request(path=path, url_param={})

    def update_category(self,
                        project_id_or_key: str,
                        category_id: int,
                        name: str,
                        ) -> Response:
        """
        カテゴリー情報の更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-category/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param category_id: カテゴリーのID
        :param name: カテゴリーの名前

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/categories/{category_id}'\
            .format(project_id_or_key=project_id_or_key, category_id=category_id)
        payloads = {'name': name}

        return self.rs.send_patch_request(path=path, request_param=payloads)

    def add_category(self,
                     project_id_or_key: str,
                     name: str,
                     ) -> Response:
        """
        カテゴリーの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-category/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param name: カテゴリーの名前

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/categories'.format(project_id_or_key=project_id_or_key)
        payloads = {'name': name}

        return self.rs.send_post_request(path=path, request_param=payloads)

    def delete_category(self,
                        project_id_or_key: str,
                        category_id: int) -> Response:
        """
        カテゴリーの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-category/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param category_id: カテゴリーのID

        :return: レスポンス
        """

        path = self.base_path + '/projects/{project_id_or_key}/categories/{category_id}'\
            .format(project_id_or_key=project_id_or_key, category_id=category_id)

        return self.rs.send_delete_request(path=path, request_param={})
