import re
from requests import Response
from typing import List, Optional, Tuple

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Project:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def add_project(self,
                    name: str,
                    key: str,
                    chart_enabled: bool,
                    subtasking_enabled: bool,
                    text_formatting_rule: str,
                    project_leader_can_edit_project_leader: Optional[bool] = None,
                    ) -> Response:
        """
        プロジェクトの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-project/

        :param name: プロジェクト名
        :param key: プロジェクトキー
        :param chart_enabled: チャートを使用するかどうか(フリープランでは利用不可)
        :param project_leader_can_edit_project_leader: プロジェクト管理者も他のプロジェクト管理者を指定可能にする
        :param subtasking_enabled: 親子課題を使用するかどうか(フリープランでは利用不可)
        :param text_formatting_rule: テキスト整形のルール backlog または markdown

        :return: レスポンス
        """

        path = self.base_path
        if re.match('^[A-Z0-9_]+$', key) is None:
            raise ValueError('Key は半角英大文字と半角数字とアンダースコアのみが使用できます')
        if text_formatting_rule not in {'backlog', 'markdown'}:
            raise ValueError('テキスト整形のルールは backlog または markdownのみが使用できます')
        # Todo: 契約プランを見て、設定できないものであれば例外を投げる
        payloads = {'name': name, 'key': key, 'chartEnabled': chart_enabled, 'subtaskingEnabled': subtasking_enabled,
                    'textFormattingRule': text_formatting_rule}
        if project_leader_can_edit_project_leader is not None:
            payloads['projectLeaderCanEditProjectLeader'] = project_leader_can_edit_project_leader

        return self.rs.send_post_request(path=path, request_param=payloads)

    def get_project(self,
                    project_id_or_key: str) -> Response:
        """
        プロジェクト情報の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-project/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/' + project_id_or_key

        return self.rs.send_get_request(path=path, url_param={})

    def update_project(self,
                       project_id_or_key: str,
                       name: Optional[str] = None,
                       key: Optional[str] = None,
                       chart_enabled: Optional[bool] = None,
                       subtasking_enabled: Optional[bool] = None,
                       project_leader_can_edit_project_leader: Optional[bool] = None,
                       text_formatting_rule: Optional[str] = None,
                       archived: Optional[bool] = None) -> Response:
        """
        プロジェクト情報の更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-project/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param name: プロジェクト名
        :param key: プロジェクトキー
        :param chart_enabled: チャートを使用するかどうか(フリープランでは利用不可)
        :param subtasking_enabled: 親子課題を使用するかどうか(フリープランでは利用不可)
        :param project_leader_can_edit_project_leader: プロジェクト管理者も他のプロジェクト管理者を指定可能にする
        :param text_formatting_rule: テキスト整形のルール backlog または markdown
        :param archived: プロジェクトの一覧に表示するかどうか

        :return: レスポンス
        """
        # Todo: 契約プランを見て、設定できないものであれば例外を投げる
        path = self.base_path + '/' + project_id_or_key
        payloads = {}
        if name is not None:
            payloads['name'] = name
        if key is not None:
            if re.match('^[A-Z0-9_]+$', key) is None:
                raise ValueError('Key は半角英大文字と半角数字とアンダースコアのみが使用できます')
            payloads['key'] = key
        if chart_enabled is not None:
            payloads['chartEnabled'] = chart_enabled
        if subtasking_enabled is not None:
            payloads['subtaskingEnabled'] = subtasking_enabled
        if project_leader_can_edit_project_leader is not None:
            payloads['projectLeaderCanEditProjectLeader'] = project_leader_can_edit_project_leader
        if text_formatting_rule is not None:
            if text_formatting_rule not in ['backlog', 'markdown']:
                raise ValueError('テキスト整形のルールは backlog または markdownのみが使用できます')
            payloads['textFormattingRule'] = text_formatting_rule
        if archived is not None:
            payloads['archived'] = archived

        return self.rs.send_patch_request(path=path, request_param=payloads)

    def delete_project(self,
                       project_id_or_key: str) -> Response:
        """
        プロジェクトの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-project/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/' + project_id_or_key

        return self.rs.send_delete_request(path=path, request_param={})

    def get_project_list(self,
                         archived: Optional[bool] = None,
                         all_projects: Optional[bool] = None) -> Response:
        """
        プロジェクト一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-project-list/

        :param archived: 省略された場合は全てのプロジェクト、falseの場合はアーカイブされていないプロジェクト、trueの場合はアーカイブされたプロジェクトを返します。
        :param all_projects: ユーザが管理者権限の場合のみ有効なパラメータです。trueの場合はすべてのプロジェクト、falseの場合は参加しているプロジェクトのみを返します。初期値はfalse。

        :return: レスポンス
        """

        path = self.base_path
        payloads = {}
        if archived is not None:
            payloads['archived'] = archived
        if all_projects is not None:
            payloads['all'] = all_projects

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_project_icon(self,
                         project_id_or_key: Optional[str] = None) -> Tuple[str, Response]:
        """
        プロジェクトアイコンの取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-project-icon/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/image'.format(project_id_or_key=project_id_or_key)

        return self.rs.get_file(path=path, url_param={})

    def get_project_recent_updates(self,
                                   project_id_or_key: str,
                                   activity_type_id: Optional[List[int]] = None,
                                   min_id: Optional[int] = None,
                                   max_id: Optional[int] = None,
                                   count: Optional[int] = 20,
                                   order: Optional[str] = 'desc',
                                   update_type: Optional[int] = None,
                                   ) -> Response:
        """
        プロジェクトの最近の活動の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-project-recent-updates/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param activity_type_id: type(1-26)
        :param min_id: 最小ID
        :param max_id: 最大ID
        :param count: 取得上限(1-100) 指定が無い場合は20
        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param update_type: 最近の更新の種別：(1)課題の追加 (2)課題の更新 (3)課題にコメント (4)課題の削除 (5)Wikiを追加 (6)Wikiを更新 (7)Wikiを削除 (8)共有ファイルを追加 (9)共有ファイルを更新(10)共有ファイルを削除 (11)Subversionコミット (12)GITプッシュ (13)GITリポジトリ作成 (14)課題をまとめて更新 (15)ユーザーがプロジェクトに参加 (16)ユーザーがプロジェクトから脱退 (17)コメントにお知らせを追加 (18)プルリクエストの追加 (19)プルリクエストの更新 (20)プルリクエストにコメント (21)プルリクエストの削除 (22)マイルストーンの追加 (23)マイルストーンの更新 (24)マイルストーンの削除 (25)グループがプロジェクトに参加 (26)グループがプロジェクトから脱退

        :return: レスポンス
        """

        path = self.base_path + '/' + project_id_or_key
        payloads = {}
        if activity_type_id is not None:
            payloads['activityTypeId[]'] = activity_type_id
        if min_id is not None:
            payloads['minId'] = min_id
        if max_id is not None:
            payloads['maxId'] = max_id
        if count is not None:
            if not 1 <= count <= 100:
                raise ValueError('count(取得上限)は1-100の範囲で指定してください')
            payloads['count'] = count
        if order is not None:
            if order not in {'desc', 'asc'}:
                raise ValueError('order は desc または asc のみが使用できます')
            payloads['order'] = order
        if update_type is not None:
            payloads['type'] = update_type

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_project_user_list(self,
                              project_id_or_key: str,
                              exclude_group_members: Optional[bool] = None) -> Response:
        """
        プロジェクトユーザー一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-project-user-list/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param exclude_group_members: グループを介してプロジェクトに参加しているメンバーを除く

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/users'.format(project_id_or_key=project_id_or_key)
        payloads = {}
        if exclude_group_members is not None:
            payloads['excludeGroupMembers'] = exclude_group_members

        return self.rs.send_get_request(path=path, url_param=payloads)

    def add_project_user(self,
                         project_id_or_key: str,
                         user_id: int) -> Response:
        """
        プロジェクトユーザーの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-project-user/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param user_id: 追加するユーザーのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/users'.format(project_id_or_key=project_id_or_key)
        payloads = {}
        if user_id is not None:
            payloads['userId'] = user_id

        return self.rs.send_post_request(path=path, request_param=payloads)

    def get_list_of_project_administrators(self,
                                           project_id_or_key: str) -> Response:
        """
        プロジェクト管理者一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-project-administrators/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/administrators'.format(project_id_or_key=project_id_or_key)

        return self.rs.send_get_request(path=path, request_param={})

    def delete_project_user(self,
                            project_id_or_key: str,
                            user_id: int) -> Response:
        """
        プロジェクトユーザーの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-project-user/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param user_id: 削除するユーザーのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/users'.format(project_id_or_key=project_id_or_key)
        payloads = {'userId': user_id}

        return self.rs.send_delete_request(path=path, request_param=payloads)

    def add_project_administrator(self,
                                  project_id_or_key: str,
                                  user_id: int) -> Response:
        """
        プロジェクト管理者の追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-project-administrator/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param user_id: 追加するユーザーのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/administrators'.format(project_id_or_key=project_id_or_key)
        payloads = {'userId': user_id}

        return self.rs.send_post_request(path=path, request_param=payloads)

    def delete_project_administrator(self,
                                     project_id_or_key: str,
                                     user_id: int) -> Response:
        """
        プロジェクト管理者の削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-project-administrator/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param user_id: 削除するユーザーのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/administrators'.format(project_id_or_key=project_id_or_key)
        payloads = {'userId': user_id}

        return self.rs.send_delete_request(path=path, request_param=payloads)


class ProjectTeam:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_project_team_list(self,
                              project_id_or_key: str,
                              ) -> Response:

        """
        プロジェクトチーム一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-project-team-list/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/teams'.format(project_id_or_key=project_id_or_key)

        return self.rs.send_get_request(path=path, url_param={})

    def add_project_team(self,
                         project_id_or_key: str,
                         team_id: Optional[int] = None,
                         ) -> Response:

        """
        プロジェクトチームの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-project-team/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param team_id: 追加するチームのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/teams'.format(project_id_or_key=project_id_or_key)
        payloads = {}
        if team_id is not None:
            payloads['teamId'] = team_id

        return self.rs.send_post_request(path=path, request_param=payloads)

    def delete_project_team(self,
                            project_id_or_key: str,
                            team_id: Optional[int] = None,
                            ) -> Response:

        """
        プロジェクトチームの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-project-team

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param team_id: 削除するチームのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/teams'.format(project_id_or_key=project_id_or_key)
        payloads = {}
        if team_id is not None:
            payloads['teamId'] = team_id

        return self.rs.send_delete_request(path=path, request_param=payloads)

    def get_project_disk_usage(self,
                               project_id_or_key: str,
                               ) -> Response:

        """
        プロジェクトの容量使用状況の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-project-disk-usage/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/diskUsage'.format(project_id_or_key=project_id_or_key)

        return self.rs.send_get_request(path=path, url_param={})
