from typing import List, Optional

from requests import Response

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Team:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'teams'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_list_of_teams(self,
                          order: str = 'desc',
                          offset: Optional[int] = None,
                          count: int = 20,
                          ) -> Response:
        """
        チーム一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-teams/

        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param offset:
        :param count: 取得上限(1-100)  指定が無い場合は20

        :return: レスポンス
        """

        path = self.base_path
        payloads = {}
        if order is not None:
            if order not in {'desc', 'asc'}:
                raise ValueError('order は desc または asc のみが使用できます')
            payloads['order'] = order
        if offset is not None:
            payloads['offset'] = offset
        if count is not None:
            if not 1 <= count <= 100:
                raise ValueError('count(取得上限)は1-100の範囲で指定してください')

        return self.rs.send_get_request(path=path, url_param=payloads)

    def add_team(self,
                 name: Optional[str] = None,
                 members: Optional[List[int]] = None,
                 ) -> Response:

        """
        チームの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-team/

        :param name: グループ名
        :param members: グループに含めるユーザーID

        :return: レスポンス
        """

        path = self.base_path
        payloads = {}
        if name is not None:
            payloads['name'] = name
        if members is not None:
            payloads['members[]'] = members

        return self.rs.send_post_request(path=path, request_param=payloads)

    def update_team(self,
                    team_id: int,
                    name: Optional[str] = None,
                    members: Optional[List[int]] = None,
                    ) -> Response:

        """
        チーム情報の更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-team/

        :param team_id: チームのID
        :param name: チーム名
        :param members: チームに含めるユーザーID

        :return: レスポンス
        """

        path = self.base_path + '{team_id}'.format(team_id=team_id)
        payloads = {}
        if name is not None:
            payloads['name'] = name
        if members is not None:
            payloads['members[]'] = members

        return self.rs.send_patch_request(path=path, request_param=payloads)

    def delete_team(self,
                    team_id: Optional[int] = None,
                    ) -> Response:

        """
        チームの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-team/

        :param team_id: チームのID

        :return: レスポンス
        """

        path = self.base_path + '{team_id}'.format(team_id=team_id)

        return self.rs.send_delete_request(path=path, request_param={})

    def get_team_icon(self,
                      team_id: Optional[int] = None,
                      ) -> Response:

        """
        チームアイコンの取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-team-icon/

        :param team_id: チームのID

        :return: レスポンス
        """

        path = self.base_path + '{team_id}/icon'.format(team_id=team_id)

        return self.rs.send_get_request(path=path, url_param={})

    def get_team(self,
                 team_id: Optional[int] = None,
                 ) -> Response:

        """
        チーム情報の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-team/

        :param team_id: チームのID

        :return: レスポンス
        """

        path = self.base_path + '{team_id}'.format(team_id=team_id)

        return self.rs.send_get_request(path=path, url_param={})
