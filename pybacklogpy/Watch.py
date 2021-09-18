from typing import List, Optional

from requests import Response

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Watch:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'watchings'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def count_watching(self,
                       user_id: int,
                       resource_already_read: Optional[bool] = None,
                       already_read: Optional[bool] = None,
                       ) -> Response:

        """
        ウォッチ数の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/count-watching/

        :param user_id: ユーザーのID
        :param resource_already_read: 既読かどうか。trueの場合は既読のウォッチ、falseの場合は未読のウォッチ、指定しない場合は両方のウォッチを返します。指定が無い場合は両方
        :param already_read: ウォッチメニューの一覧表示後に更新されたウォッチの件数を返します。trueの場合はウォッチメニューを表示した後に更新されていない(既読状態の)件数を返します。falseの場合はウォッチメニューを表示した後に更新された(未読状態の)ウォッチの件数を返します。指定が無い場合は両方を合わせた件数を返します。resourceAlreadyReadが指定してある場合、alreadyReadは使用されません。

        :return: レスポンス
        """

        path = 'users/{user_id}/watchings/count'.format(user_id=user_id)
        payloads = {}
        if resource_already_read is not None:
            payloads['resourceAlreadyRead'] = resource_already_read
        if already_read is not None:
            payloads['alreadyRead'] = already_read

        return self.rs.send_get_request(path=path, url_param=payloads)

    def mark_watching_as_read(self,
                              watching_id: int,
                              ) -> Response:

        """
        ウォッチの既読化
        https://developer.nulab.com/ja/docs/backlog/api/2/mark-watching-as-read/

        :param watching_id: ウォッチのID

        :return: レスポンス
        """

        path = self.base_path + '/{watching_id}/markAsRead'.format(watching_id=watching_id)

        return self.rs.send_get_request(path=path, url_param={})

    def add_watching(self,
                     issue_id_or_key: Optional[str] = None,
                     note: Optional[str] = None,
                     ) -> Response:

        """
        ウォッチの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-watching/

        :param issue_id_or_key: 課題のID または 課題キー
        :param note: メモ

        :return: レスポンス
        """

        path = self.base_path
        payloads = {}
        if issue_id_or_key is not None:
            payloads['issueIdOrKey'] = issue_id_or_key
        if note is not None:
            payloads['note'] = note

        return self.rs.send_post_request(path=path, request_param=payloads)

    def get_watching(self,
                     watching_id: int,
                     ) -> Response:

        """
        ウォッチ情報の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-watching/

        :param watching_id: ウォッチのID

        :return: レスポンス
        """

        path = self.base_path + '/{watching_id}'.format(watching_id=watching_id)

        return self.rs.send_get_request(path=path, url_param={})

    def delete_watching(self,
                        watching_id: int,
                        ) -> Response:

        """
        ウォッチの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-watching/

        :param watching_id: ウォッチのID

        :return: レスポンス
        """

        path = self.base_path + '/{watching_id}'.format(watching_id=watching_id)

        return self.rs.send_delete_request(path=path, request_param={})

    def update_watching(self,
                        watching_id: int,
                        note: Optional[str] = None,
                        ) -> Response:

        """
        ウォッチの更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-watching/

        :param watching_id: ウォッチのID
        :param note: メモ

        :return: レスポンス
        """

        path = self.base_path + '/{watching_id}'.format(watching_id=watching_id)
        payloads = {}
        if note is not None:
            payloads['note'] = note

        return self.rs.send_post_request(path=path, request_param=payloads)

    def get_watching_list(self,
                          user_id: int,
                          order: str = 'desc',
                          sort: str = 'issueUpdated',
                          count: int = 20,
                          offset: Optional[int] = None,
                          resource_already_read: Optional[bool] = None,
                          issue_id: Optional[List[int]] = None,
                          ) -> Response:

        """
        ウォッチ一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-watching-list/

        :param user_id: ユーザーのID
        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param sort: ウォッチ一覧のソートに使用する属性名“created”“updated”“issueUpdated”指定が無い場合は”issueUpdated”
        :param count: 取得上限(1-100) 指定が無い場合は20
        :param offset:
        :param resource_already_read: ウォッチしている課題の詳細を既読かどうか。trueの場合は既読のウォッチ、falseの場合は未読のウォッチ、指定しない場合は両方のウォッチを返します。指定が無い場合は両方
        :param issue_id: 課題のID

        :return: レスポンス
        """

        path = 'users/{user_id}/watchings'.format(user_id=user_id)

        payloads = {}
        if order is not None:
            if order not in {'desc', 'asc'}:
                raise ValueError('order は desc または asc のみが使用できます')
            payloads['order'] = order
        if sort is not None:
            payloads['sort'] = sort
        if count is not None:
            if not 1 <= count <= 100:
                raise ValueError('count(取得上限)は1-100の範囲で指定してください')
            payloads['count'] = count
        if offset is not None:
            payloads['offset'] = offset
        if resource_already_read is not None:
            payloads['resourceAlreadyRead'] = resource_already_read
        if issue_id is not None:
            payloads['issueId[]'] = issue_id

        return self.rs.send_get_request(path=path, url_param=payloads)
