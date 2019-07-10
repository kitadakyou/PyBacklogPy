from requests import Response
from typing import List, Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Webhook:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_list_of_webhooks(self,
                             project_id_or_key: str
                             ) -> Response:
        """
        Webhook一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-webhooks/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/webhooks'.format(project_id_or_key=project_id_or_key)

        return self.rs.send_get_request(path=path, url_param={})

    def get_webhook(self,
                    project_id_or_key: str,
                    webhook_id: str,
                    ) -> Response:
        """
        Webhookの取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-webhook/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param webhook_id: WebhookのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/webhooks/{webhook_id}'\
            .format(project_id_or_key=project_id_or_key, webhook_id=webhook_id)

        return self.rs.send_get_request(path=path, url_param={})

    def update_webhook(self,
                       project_id_or_key: str,
                       webhook_id: str,
                       name: Optional[str] = None,
                       description: Optional[str] = None,
                       hook_url: Optional[str] = None,
                       all_event: Optional[bool] = None,
                       activity_type_ids: Optional[List[int]] = None,
                       ) -> Response:
        """
        Webhookの更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-webhook/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param webhook_id: WebhookのID
        :param name: 名前
        :param description: 詳細
        :param hook_url: hook URL
        :param all_event: 全てのイベントを通知
        :param activity_type_ids: 通知するイベントのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/webhooks/{webhook_id}'\
            .format(project_id_or_key=project_id_or_key, webhook_id=webhook_id)

        payloads = {}
        if name is not None:
            payloads['name'] = name
        if description is not None:
            payloads['description'] = description
        if hook_url is not None:
            payloads['hookUrl'] = hook_url
        if all_event is not None:
            payloads['allEvent'] = all_event
        if activity_type_ids is not None:
            payloads['activityTypeIds[]'] = activity_type_ids

        return self.rs.send_patch_request(path=path, request_param=payloads)

    def add_webhook(self,
                    project_id_or_key: str,
                    name: Optional[str] = None,
                    description: Optional[str] = None,
                    hook_url: Optional[str] = None,
                    all_event: Optional[bool] = None,
                    activity_type_ids: Optional[List[int]] = None,
                    ) -> Response:
        """
        Webhookの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-webhook/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param name: 名前
        :param description: 詳細
        :param hook_url: hook URL
        :param all_event: 全てのイベントを通知
        :param activity_type_ids: 通知するイベントのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/webhooks'.format(project_id_or_key=project_id_or_key)

        payloads = {}
        if name is not None:
            payloads['name'] = name
        if description is not None:
            payloads['description'] = description
        if hook_url is not None:
            payloads['hookUrl'] = hook_url
        if all_event is not None:
            payloads['allEvent'] = all_event
        if activity_type_ids is not None:
            payloads['activityTypeIds[]'] = activity_type_ids

        return self.rs.send_post_request(path=path, request_param=payloads)

    def delete_webhook(self,
                       project_id_or_key: str,
                       webhook_id: str,
                       ) -> Response:
        """
        Webhookの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-webhook/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param webhook_id: WebhookのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/webhooks/{webhook_id}' \
            .format(project_id_or_key=project_id_or_key, webhook_id=webhook_id)

        return self.rs.send_delete_request(path=path, request_param={})
