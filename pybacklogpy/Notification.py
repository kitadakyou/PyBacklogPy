from typing import Optional

from requests import Response

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Notification:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'notifications'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_notification(self,
                         min_id: Optional[int] = None,
                         max_id: Optional[int] = None,
                         count: Optional[int] = 20,
                         order: Optional[str] = 'desc',
                         sender_id: Optional[int] = None,
                         ) -> Response:
        """
        お知らせ一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-notification/

        :param min_id: 最小ID
        :param max_id: 最大ID
        :param count: 取得上限(1-100) 指定が無い場合は20
        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param sender_id: 送信者ID

        :return: レスポンス
        """

        path = self.base_path
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
        if sender_id is not None:
            payloads['senderId'] = sender_id

        return self.rs.send_get_request(path=path, url_param=payloads)

    def count_notification(self,
                           already_read: Optional[bool] = None,
                           resource_already_read: Optional[bool] = None,
                           ) -> Response:
        """
        お知らせ数の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/count-notification/

        :param already_read:
        :param resource_already_read:

        :return: レスポンス
        """

        path = self.base_path + '/count'
        payloads = {}
        if already_read is not None:
            payloads['alreadyRead'] = already_read
        if resource_already_read is not None:
            payloads['resourceAlreadyRead'] = resource_already_read

        return self.rs.send_get_request(path=path, url_param=payloads)

    def read_notification(self,
                          notification_id: int,
                          ) -> Response:
        """
        お知らせの既読化
        https://developer.nulab.com/ja/docs/backlog/api/2/read-notification/

        :param notification_id: お知らせのID

        :return: レスポンス
        """

        path = self.base_path + '/{notification_id}/markAsRead'.format(notification_id=str(notification_id))

        return self.rs.send_post_request(path=path, request_param={})

    def reset_unread_notification_count(self,
                                        ):
        """
        お知らせ数のリセット
        https://developer.nulab.com/ja/docs/backlog/api/2/reset-unread-notification-count/

        :return: レスポンス
        """

        path = self.base_path + '/markAsRead'

        return self.rs.send_post_request(path=path, request_param={})
