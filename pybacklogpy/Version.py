from requests import Response
from typing import Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Version:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_version_milestone_list(self,
                                   project_id_or_key: Optional[str] = None,
                                   ) -> Response:

        """
        バージョン(マイルストーン)一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-version-milestone-list/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/versions'.format(project_id_or_key=project_id_or_key)

        return self.rs.send_get_request(path=path, url_param={})

    def update_version_milestone(self,
                                 project_id_or_key: str,
                                 version_id: int,
                                 name: str,
                                 description: Optional[str] = None,
                                 start_date: Optional[str] = None,
                                 release_due_date: Optional[str] = None,
                                 archived: Optional[bool] = None,
                                 ) -> Response:

        """
        バージョン(マイルストーン)情報の更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-version-milestone/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param version_id: バージョンのID
        :param name: バージョンの名前
        :param description: バージョンの説明
        :param start_date: バージョンの開始日 (yyyy-MM-dd)
        :param release_due_date: バージョンのリリース予定日 (yyyy-MM-dd)
        :param archived: プロジェクトホームに表示しない場合はtrue

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/versions/{version_id}'\
            .format(project_id_or_key=project_id_or_key, version_id=version_id)
        payloads = {'name': name}
        if description is not None:
            payloads['description'] = description
        if start_date is not None:
            payloads['startDate'] = start_date
        if release_due_date is not None:
            payloads['releaseDueDate'] = release_due_date
        if archived is not None:
            payloads['archived'] = archived

        return self.rs.send_patch_request(path=path, request_param=payloads)

    def delete_version(self,
                       project_id_or_key: Optional[str] = None,
                       version_id: Optional[int] = None,
                       ) -> Response:

        """
        バージョン(マイルストーン)の削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-version/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param version_id: バージョンのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/versions/{version_id}'\
            .format(project_id_or_key=project_id_or_key, version_id=version_id)

        return self.rs.send_delete_request(path=path, request_param={})

    def add_version_milestone(self,
                              project_id_or_key: str,
                              name: str,
                              description: Optional[str] = None,
                              start_date: Optional[str] = None,
                              release_due_date: Optional[str] = None,
                              ) -> Response:

        """
        バージョン(マイルストーン)の追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-version-milestone/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param name: バージョンの名前
        :param description: バージョンの説明
        :param start_date: バージョンの開始日 (yyyy-MM-dd)
        :param release_due_date: バージョンのリリース予定日 (yyyy-MM-dd)

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/versions'.format(project_id_or_key=project_id_or_key)
        payloads = {'name': name}
        if description is not None:
            payloads['description'] = description
        if start_date is not None:
            payloads['startDate'] = start_date
        if release_due_date is not None:
            payloads['releaseDueDate'] = release_due_date

        return self.rs.send_post_request(path=path, request_param=payloads)
