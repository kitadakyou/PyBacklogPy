from requests import Response
from typing import Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class GitRepository:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_list_of_git_repositories(self,
                                     project_id_or_key: str,
                                     ) -> Response:
        """
        Gitリポジトリ一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-git-repositories/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories'.format(project_id_or_key=project_id_or_key)
        return self.rs.send_get_request(path=path, url_param={})

    def get_git_repository(self,
                           project_id_or_key: str,
                           repo_id_or_name: str,
                           ) -> Response:
        """
        Gitリポジトリの取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-git-repository/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}'\
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name)

        return self.rs.send_get_request(path=path, url_param={})
