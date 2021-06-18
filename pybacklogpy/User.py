from datetime import datetime
import re
from requests import Response
from typing import List, Optional, Tuple

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class User:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'users'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_user_list(self) -> Response:
        """
        ユーザー一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-user-list/

        :return: レスポンス
        """

        path = self.base_path
        return self.rs.send_get_request(path=path, url_param={})

    def get_user(self,
                 user_id: int) -> Response:
        """
        ユーザー情報の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-user/

        :param user_id: ユーザーのID

        :return: レスポンス
        """

        path = self.base_path + '/{user_id}'.format(user_id=user_id)

        return self.rs.send_get_request(path=path, url_param={})

    def get_own_user(self) -> Response:
        """
        認証ユーザー情報の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-own-user/

        :return: レスポンス
        """

        path = self.base_path + '/myself'
        return self.rs.send_get_request(path=path, url_param={})

    def get_user_icon(self,
                      user_id: int) -> Tuple[str, Response]:
        """
        ユーザーアイコンの取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-user-icon/

        :param user_id: ユーザーのID

        :return: (保存された画像のPATH, backlog上の画像url)
        """

        path = self.base_path + '/{user_id}/icon'.format(user_id=str(user_id))

        response = self.rs.send_get_request(path=path, url_param={})
        if not response.ok:
            return '', response
        # ユーザーアイコンだけ他と戻り値のパターンが違うので、個別対応
        filename = response.url.split('/')[len(response.url.split('/')) - 1]
        filepath = 'tmp/{filename}'.format(filename=filename)
        with open(filepath, mode='wb') as save_file:
            save_file.write(response.content)
        return filepath, response

    def get_user_recent_updates(self,
                                user_id: int,
                                activity_type_id: Optional[List[int]] = None,
                                min_id: Optional[int] = None,
                                max_id: Optional[int] = None,
                                count: Optional[int] = 20,
                                order: Optional[str] = 'desc',
                                ) -> Response:
        """
        ユーザーの最近の活動の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-user-recent-updates/

        :param user_id: ユーザーのID
        :param activity_type_id: type (1)課題の追加 (2)課題の更新 (3)課題にコメント (4)課題の削除 (5)Wikiを追加 (6)Wikiを更新 (7)Wikiを削除 (8)共有ファイルを追加 (9)共有ファイルを更新(10)共有ファイルを削除 (11)Subversionコミット (12)GITプッシュ (13)GITリポジトリ作成 (14)課題をまとめて更新 (15)ユーザーがプロジェクトに参加 (16)ユーザーがプロジェクトから脱退 (17)コメントにお知らせを追加
        :param min_id: 最小ID
        :param max_id: 最大ID
        :param count: 取得上限(1-100) 指定が無い場合は20
        :param order: “asc”または”desc” 指定が無い場合は”desc”

        :return: レスポンス
        """

        path = self.base_path + '/{user_id}/activities'.format(user_id=user_id)
        payloads = {}
        if activity_type_id is not None:
            if min(activity_type_id) < 1 or 17 < max(activity_type_id):
                raise ValueError('activityTypeIdは1-17の範囲で指定してください')
            payloads['activityTypeId[]'] = activity_type_id
        if min_id is not None:
            payloads['minId'] = min_id
        if max_id is not None:
            payloads['maxId'] = max_id
        if count is not None:
            if not 1 <= count <= 100:
                raise ValueError('count(取得上限)は1-100の範囲で指定してください')
        if order is not None:
            if order is not None:
                if order not in {'desc', 'asc'}:
                    raise ValueError('order は desc または asc のみが使用できます')
            payloads['order'] = order

        return self.rs.send_get_request(path=path, url_param=payloads)

    def count_user_received_stars(self,
                                  user_id: int,
                                  since: Optional[str] = None,
                                  until: Optional[str] = None) -> Response:
        """
        ユーザーの受け取ったスターの数の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/count-user-received-stars/

        :param user_id: ユーザーのID
        :param since: 指定した日付以降のスターをカウント (yyyy-MM-dd)
        :param until: 指定した日付以前のスターをカウント (yyyy-MM-dd)

        :return: レスポンス
        """

        path = self.base_path + '/{user_id}/stars/count'.format(user_id=user_id)
        payloads = {}
        if since is not None:
            if re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', since) is None:
                raise ValueError('日付の形式はyyyy-MM-ddです')
            try:
                datetime.strptime(since, '%Y-%m-%d')  # docで「0埋めした」って言ってるのに2000-1-1みたいなの通すんじゃねぇよ💢
            except ValueError:
                raise ValueError('日付の形式はyyyy-MM-ddです')
            else:
                payloads['since'] = since
        if until is not None:
            if re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', until) is None:
                raise ValueError('日付の形式はyyyy-MM-ddです')
            try:
                datetime.strptime(until, '%Y-%m-%d')
            except ValueError:
                raise ValueError('日付の形式はyyyy-MM-ddです')
            else:
                payloads['until'] = until

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_received_star_list(self,
                               user_id: int,
                               min_id: Optional[int] = None,
                               max_id: Optional[int] = None,
                               count: Optional[int] = 20,
                               order: Optional[str] = 'desc') -> Response:
        """
        ユーザーの受け取ったスター一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-received-star-list/

        :param user_id: ユーザーのID
        :param min_id: 最小ID
        :param max_id: 最大ID
        :param count: 取得上限(1-100) 指定が無い場合は20
        :param order: “asc”または”desc” 指定が無い場合は”desc”

        :return: レスポンス
        """

        path = self.base_path + '/{user_id}/stars'.format(user_id=user_id)
        payloads = {}
        if min_id is not None:
            payloads['minId'] = min_id
        if max_id is not None:
            payloads['maxId'] = max_id
        if count is not None:
            if not 1 <= count <= 100:
                raise ValueError('count(取得上限)は1-100の範囲で指定してください')
        if order is not None:
            if order not in {'desc', 'asc'}:
                raise ValueError('order は desc または asc のみが使用できます')
            payloads['order'] = order

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_list_of_recently_viewed_issues(self,
                                           order: Optional[str] = 'desc',
                                           offset: Optional[int] = None,
                                           count: Optional[int] = 20) -> Response:
        """
        自分が最近見た課題一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-recently-viewed-issues/

        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param offset:
        :param count: 取得上限(1-100)  指定が無い場合は20

        :return: レスポンス
        """

        path = self.base_path + '/myself/recentlyViewedIssues'
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

    def get_list_of_recently_viewed_projects(self,
                                             order: Optional[str] = 'desc',
                                             offset: Optional[int] = None,
                                             count: Optional[int] = 20) -> Response:
        """
        自分が最近見たプロジェクト一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-recently-viewed-projects/

        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param offset:
        :param count: 取得上限(1-100)  指定が無い場合は20

        :return: レスポンス
        """

        path = self.base_path + '/myself/recentlyViewedProjects'
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

    def get_list_of_recently_viewed_wikis(self,
                                          order: Optional[str] = 'desc',
                                          offset: Optional[int] = None,
                                          count: Optional[int] = 20) -> Response:
        """
        自分が最近見たWiki一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-recently-viewed-wikis/

        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param offset:
        :param count: 取得上限(1-100)  指定が無い場合は20

        :return: レスポンス
        """

        path = self.base_path + '/myself/recentlyViewedWikis'
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
