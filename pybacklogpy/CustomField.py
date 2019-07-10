from requests import Response
from typing import List, Optional

from pybacklogpy.const import CUSTOM_FIELD_TYPE
from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class CustomField:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_custom_field_list(self,
                              project_id_or_key: Optional[str] = None,
                              ) -> Response:

        """
        カスタム属性一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-custom-field-list/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/customFields'.format(project_id_or_key=project_id_or_key)

        return self.rs.send_get_request(path=path, url_param={})

    def add_custom_field(self,
                         project_id_or_key: str,
                         type_id: int,
                         name: str,
                         applicable_issue_types: Optional[List[int]] = None,
                         description: Optional[str] = None,
                         required: Optional[bool] = None,
                         min_num: Optional[int] = None,
                         max_num: Optional[int] = None,
                         min_date: Optional[str] = None,
                         max_date: Optional[str] = None,
                         initial_value: Optional[int] = None,
                         unit: Optional[str] = None,
                         initial_value_type: Optional[int] = None,
                         initial_date: Optional[str] = None,
                         initial_shift: Optional[int] = None,
                         items: List[str] = None,
                         allow_input: Optional[bool] = None,
                         allow_add_item: Optional[bool] = None,
                         ) -> Response:

        """
        カスタム属性の追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-custom-field/
        
        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param type_id: カスタム属性の形式 (1)文字列 (2)文章 (3)数値 (4)日付 (5)単一リスト (6)複数リスト (7)チェックボックス (8)ラジオ
        :param name: カスタム属性の名前
        :param applicable_issue_types: カスタム属性を有効にする種別ID空の場合、すべての課題種別で有効
        :param description: カスタム属性の説明
        :param required: 必須な属性とする場合はtrue
        :param min_num: 最小値
        :param max_num: 最大値
        :param min_date: 最小値 (yyyy-MM-dd)
        :param max_date: 最大値 (yyyy-MM-dd)
        :param initial_value: 初期値
        :param unit: 単位
        :param initial_value_type: 1:当日 2: 当日 + initialShift 3:指定日
        :param initial_date: 初期値 (yyyy-MM-dd)
        :param initial_shift: 差分日数
        :param items: リスト項目
        :param allow_input: その他直接入力を許可
        :param allow_add_item: 項目の追加を許可
        
        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/customFields'.format(project_id_or_key=project_id_or_key)
        payloads = {'typeId': type_id, 'name': name}
        if applicable_issue_types is not None:
            payloads['applicableIssueTypes[]'] = applicable_issue_types
        if description is not None:
            payloads['description'] = description
        if required is not None:
            payloads['required'] = required

        if type_id == CUSTOM_FIELD_TYPE['数値']:
            if min_num is not None:
                payloads['min'] = min_num
            if max_num is not None:
                payloads['max'] = max_num
            if initial_value is not None:
                payloads['initialValue'] = initial_value
            if unit is not None:
                payloads['unit'] = unit
        if type_id == CUSTOM_FIELD_TYPE['日付']:
            if min_date is not None:
                payloads['min'] = min_date
            if max_date is not None:
                payloads['max'] = max_date
            if initial_value_type is not None:
                payloads['initialValueType'] = initial_value_type
            if initial_date is not None:
                payloads['initialDate'] = initial_date
            if initial_shift is not None:
                payloads['initialShift'] = initial_shift
        if type_id in (CUSTOM_FIELD_TYPE['単一リスト'],
                       CUSTOM_FIELD_TYPE['複数リスト'],
                       CUSTOM_FIELD_TYPE['チェックボックス'],
                       CUSTOM_FIELD_TYPE['ラジオ'],):
            if items is not None:
                payloads['items[]'] = items
            if allow_input is not None:
                payloads['allowInput'] = allow_input
            if allow_add_item is not None:
                payloads['allowAddItem'] = allow_add_item

        return self.rs.send_post_request(path=path, request_param=payloads)

    def update_custom_field(self,
                            project_id_or_key: str,
                            custom_field_id: int,
                            name: Optional[str] = None,
                            applicable_issue_types: Optional[List[int]] = None,
                            description: Optional[str] = None,
                            required: Optional[bool] = None,
                            min_num: Optional[int] = None,
                            max_num: Optional[int] = None,
                            min_date: Optional[str] = None,
                            max_date: Optional[str] = None,
                            initial_value: Optional[int] = None,
                            unit: Optional[str] = None,
                            initial_value_type: Optional[int] = None,
                            initial_date: Optional[str] = None,
                            initial_shift: Optional[int] = None,
                            items: Optional[List[str]] = None,
                            allow_input: Optional[bool] = None,
                            allow_add_item: Optional[bool] = None,
                            ) -> Response:

        """
        カスタム属性の更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-custom-field/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param custom_field_id: カスタム属性のID
        :param name: カスタム属性の名前
        :param applicable_issue_types: カスタム属性を有効にする種別ID空の場合、すべての課題種別で有効
        :param description: カスタム属性の説明
        :param required: 必須な属性とする場合はtrue
        :param min_num: 最小値
        :param max_num: 最大値
        :param min_date: 最小値 (yyyy-MM-dd)
        :param max_date: 最大値 (yyyy-MM-dd)
        :param initial_value: 初期値
        :param unit: 単位
        :param initial_value_type: (1) 当日 (2) 当日 + initialShift (3)指定日
        :param initial_date: 初期値 (yyyy-MM-dd)
        :param initial_shift: 差分日数
        :param items: リスト項目
        :param allow_input: その他直接入力を許可
        :param allow_add_item: 項目の追加を許可

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/customFields/{custom_field_id}'\
            .format(project_id_or_key=project_id_or_key, custom_field_id=custom_field_id)
        payloads = {}
        # TODO: 一度 GET して適切な type_id で分岐
        if name is not None:
            payloads['name'] = name
        if applicable_issue_types is not None:
            payloads['applicableIssueTypes[]'] = applicable_issue_types
        if description is not None:
            payloads['description'] = description
        if required is not None:
            payloads['required'] = required
        if min_num is not None:
            payloads['min'] = min_num
        if max_num is not None:
            payloads['max'] = max_num
        if initial_value is not None:
            payloads['initialValue'] = initial_value
        if unit is not None:
            payloads['unit'] = unit
        if min_date is not None:
            payloads['min'] = min_date
        if max_date is not None:
            payloads['max'] = max_date
        if initial_value_type is not None:
            payloads['initialValueType'] = initial_value_type
        if initial_date is not None:
            payloads['initialDate'] = initial_date
        if initial_shift is not None:
            payloads['initialShift'] = initial_shift
        if items is not None:
            payloads['items[]'] = items
        if allow_input is not None:
            payloads['allowInput'] = allow_input
        if allow_add_item is not None:
            payloads['allowAddItem'] = allow_add_item

        return self.rs.send_patch_request(path=path, request_param=payloads)

    def delete_custom_field(self,
                            project_id_or_key: Optional[str] = None,
                            custom_field_id: Optional[int] = None,
                            ) -> Response:
        """
        カスタム属性の削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-custom-field/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param custom_field_id: カスタム属性のID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/customFields/{custom_field_id}' \
            .format(project_id_or_key=project_id_or_key, custom_field_id=custom_field_id)

        return self.rs.send_delete_request(path=path, request_param={})


class ListTypeCustomField:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def add_list_item_for_list_type_custom_field(self,
                                                 project_id_or_key: Optional[str] = None,
                                                 custom_field_id: Optional[int] = None,
                                                 name: Optional[str] = None,
                                                 ) -> Response:

        """
        選択リストカスタム属性のリスト項目の追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-list-item-for-list-type-custom-field/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param custom_field_id: カスタム属性のID
        :param name: リスト項目の名前

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/customFields/{custom_field_id}/items'\
            .format(project_id_or_key=project_id_or_key, custom_field_id=custom_field_id)
        payloads = {'name': name}

        return self.rs.send_post_request(path=path, request_param=payloads)

    def delete_list_item_for_list_type_custom_field(self,
                                                    project_id_or_key: str,
                                                    custom_field_id: int,
                                                    item_id: int
                                                    ) -> Response:

        """
        選択リストカスタム属性のリスト項目の削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-list-item-for-list-type-custom-field/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param custom_field_id: カスタム属性のID
        :param item_id: リスト項目のID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/customFields/{custom_field_id}/items/{item_id}'\
            .format(project_id_or_key=project_id_or_key, custom_field_id=custom_field_id, item_id=item_id)

        return self.rs.send_delete_request(path=path, request_param={})

    def update_list_item_for_list_type_custom_field(self,
                                                    project_id_or_key: Optional[str] = None,
                                                    custom_field_id: Optional[int] = None,
                                                    item_id: Optional[int] = None,
                                                    name: Optional[str] = None,
                                                    ) -> Response:

        """
        選択リストカスタム属性のリスト項目の更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-list-item-for-list-type-custom-field/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param custom_field_id: カスタム属性のID
        :param item_id: リスト項目のID
        :param name: リスト項目の名前

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/customFields/{custom_field_id}/items/{item_id}'\
            .format(project_id_or_key=project_id_or_key, custom_field_id=custom_field_id, item_id=item_id)
        payloads = {}
        if name is not None:
            payloads['name'] = name

        return self.rs.send_patch_request(path=path, request_param=payloads)
