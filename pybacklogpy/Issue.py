import re
from requests import Response
from typing import Dict, List, Optional, Tuple

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Issue:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'issues'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_issue_list(self,
                       project_id: Optional[List[int]] = None,
                       issue_type_id: Optional[List[int]] = None,
                       category_id: Optional[List[int]] = None,
                       version_id: Optional[List[int]] = None,
                       milestone_id: Optional[List[int]] = None,
                       status_id: Optional[List[int]] = None,
                       priority_id: Optional[List[int]] = None,
                       assignee_id: Optional[List[int]] = None,
                       created_user_id: Optional[List[int]] = None,
                       resolution_id: Optional[List[int]] = None,
                       parent_child: Optional[int] = None,
                       attachment: Optional[bool] = None,
                       shared_file: Optional[bool] = None,
                       sort: Optional[str] = None,
                       order: Optional[str] = 'desc',
                       offset: Optional[int] = None,
                       count: Optional[int] = 20,
                       created_since: Optional[str] = None,
                       created_until: Optional[str] = None,
                       updated_since: Optional[str] = None,
                       updated_until: Optional[str] = None,
                       start_date_since: Optional[str] = None,
                       start_date_until: Optional[str] = None,
                       due_date_since: Optional[str] = None,
                       due_date_until: Optional[str] = None,
                       id_: Optional[List[int]] = None,
                       parent_issue_id: Optional[List[int]] = None,
                       keyword: Optional[str] = None,
                       custom_field_text: Dict[int, str] = None,
                       custom_field_num: Dict[int, Dict[str, int or None]] = None,
                       custom_field_date: Dict[int, Dict[str, int or None]] = None,
                       custom_field_list: Dict[int, List[int]] = None) -> Response:
        """
        課題一覧の取得
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-issue-list/

        :param project_id: プロジェクトのID
        :param issue_type_id: 種別のID
        :param category_id: カテゴリーのID
        :param version_id: 発生バージョンのID
        :param milestone_id: マイルストーンのID
        :param status_id: 状態のID
        :param priority_id: 優先度のID
        :param assignee_id: 担当者のID
        :param created_user_id: 登録者のID
        :param resolution_id: 完了理由のID
        :param parent_child: 親子課題の 0:すべて, 1:子課題以外, 2:子課題, 3:親課題でも子課題でもない課題, 4:親課題
        :param attachment: 添付ファイルを含む場合はtrue
        :param shared_file: 共有ファイルを含む場合はtrue
        :param sort: 課題一覧のソートに使用する属性名
        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param offset: オフセット
        :param count: 取得上限(1-100)  指定が無い場合は20
        :param created_since: 登録日 (yyyy-MM-dd)
        :param created_until: 登録日 (yyyy-MM-dd)
        :param updated_since: 更新日 (yyyy-MM-dd)
        :param updated_until: 更新日 (yyyy-MM-dd)
        :param start_date_since: 開始日 (yyyy-MM-dd)
        :param start_date_until: 開始日 (yyyy-MM-dd)
        :param due_date_since: 期限日 (yyyy-MM-dd)
        :param due_date_until: 期限日 (yyyy-MM-dd)
        :param id_: 課題のID
        :param parent_issue_id: 親課題のID
        :param keyword: 検索キーワード
        :param custom_field_text: カスタム属性(テキスト)の検索キーワード  e.g.) {1: 'debug', 2: 'top'}
        :param custom_field_num: カスタム属性(数値)の最小・最大値  e.g.) {1: {'min': 10, 'max': 20}, 2: {'min': None, 'max': 100}}
        :param custom_field_date: カスタム属性(日付)の最小・最大値  e.g.) {1: {'min': '2000-01-01', max: '2000-12-31'}}
        :param custom_field_list: カスタム属性(リスト)の指定ID  e.g.) {1: [100, 101, 102], 2: [200]}
        :return: レスポンス
        """
        path = self.base_path
        payloads = {}
        if project_id is not None:
            payloads['projectId[]'] = project_id
        if issue_type_id is not None:
            payloads['issueTypeId[]'] = issue_type_id
        if category_id is not None:
            payloads['categoryId[]'] = category_id
        if version_id is not None:
            payloads['versionId[]'] = version_id
        if milestone_id is not None:
            payloads['milestoneId[]'] = milestone_id
        if status_id is not None:
            payloads['statusId[]'] = status_id
        if priority_id is not None:
            payloads['priorityId[]'] = priority_id
        if assignee_id is not None:
            payloads['assigneeId[]'] = assignee_id
        if created_user_id is not None:
            payloads['createdUserId[]'] = created_user_id
        if resolution_id is not None:
            payloads['resolutionId[]'] = resolution_id
        if parent_child is not None:
            payloads['parentChild'] = parent_child
        if attachment is not None:
            payloads['attachment'] = attachment
        if shared_file is not None:
            payloads['sharedFile'] = shared_file
        if sort is not None:
            payloads['sort'] = sort
        if order is not None:
            if order not in {'desc', 'asc'}:
                raise ValueError('order は desc または asc のみが使用できます')
            payloads['order'] = order
        if offset is not None:
            payloads['offset'] = offset
        if count is not None:
            if not 1 <= count <= 100:
                raise ValueError('count(取得上限)は1-100の範囲で指定してください')
            payloads['count'] = count
        if created_since is not None:
            payloads['createdSince'] = created_since
        if created_until is not None:
            payloads['createdUntil'] = created_until
        if updated_since is not None:
            payloads['updatedSince'] = updated_since
        if updated_until is not None:
            payloads['updatedUntil'] = updated_until
        if start_date_since is not None:
            payloads['startDateSince'] = start_date_since
        if start_date_until is not None:
            payloads['startDateUntil'] = start_date_until
        if due_date_since is not None:
            payloads['dueDateSince'] = due_date_since
        if due_date_until is not None:
            payloads['dueDateUntil'] = due_date_until
        if id_ is not None:
            payloads['id[]'] = id_
        if parent_issue_id is not None:
            payloads['parentIssueId[]'] = parent_issue_id
        if keyword is not None:
            payloads['keyword'] = keyword
        if custom_field_text is not None:
            for field_id in custom_field_text:
                payloads['customField_{field_id}'.format(field_id=field_id)] = custom_field_text[field_id]
        if custom_field_num is not None:
            for field_id in custom_field_num:
                if custom_field_num[field_id]['min']:
                    payloads['customField_{field_id}_min'.format(field_id=field_id)] = custom_field_num[field_id]['min']
                if custom_field_num[field_id]['max']:
                    payloads['customField_{field_id}_max'.format(field_id=field_id)] = custom_field_num[field_id]['max']
        if custom_field_date is not None:
            for field_id in custom_field_date:
                if custom_field_date[field_id]['min']:
                    payloads['customField_{field_id}_min'.format(field_id=field_id)] = custom_field_date[field_id][
                        'min']
                if custom_field_date[field_id]['max']:
                    payloads['customField_{field_id}_max'.format(field_id=field_id)] = custom_field_date[field_id][
                        'max']
        if custom_field_list is not None:
            for field_id in custom_field_list:
                payloads['customField_{field_id}[]'.format(field_id=field_id)] = custom_field_list[field_id]

        return self.rs.send_get_request(path=path, url_param=payloads)

    def count_issue(self,
                    project_id: Optional[List[int]] = None,
                    issue_type_id: Optional[List[int]] = None,
                    category_id: Optional[List[int]] = None,
                    version_id: Optional[List[int]] = None,
                    milestone_id: Optional[List[int]] = None,
                    status_id: Optional[List[int]] = None,
                    priority_id: Optional[List[int]] = None,
                    assignee_id: Optional[List[int]] = None,
                    created_user_id: Optional[List[int]] = None,
                    resolution_id: Optional[List[int]] = None,
                    parent_child: Optional[int] = None,
                    attachment: Optional[bool] = None,
                    shared_file: Optional[bool] = None,
                    sort: Optional[str] = None,
                    order: Optional[str] = 'desc',
                    offset: Optional[int] = None,
                    count: Optional[int] = 20,
                    created_since: Optional[str] = None,
                    created_until: Optional[str] = None,
                    updated_since: Optional[str] = None,
                    updated_until: Optional[str] = None,
                    start_date_since: Optional[str] = None,
                    start_date_until: Optional[str] = None,
                    due_date_since: Optional[str] = None,
                    due_date_until: Optional[str] = None,
                    id_: Optional[List[int]] = None,
                    parent_issue_id: Optional[List[int]] = None,
                    keyword: Optional[str] = None,
                    custom_field_text: Dict[int, str] = None,
                    custom_field_num: Dict[int, Dict[str, int or None]] = None,
                    custom_field_date: Dict[int, Dict[str, int or None]] = None,
                    custom_field_list: Dict[int, List[int]] = None) -> Response:
        """
        課題数の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/count-issue/

        :param project_id: プロジェクトのID
        :param issue_type_id: 種別のID
        :param category_id: カテゴリーのID
        :param version_id: 発生バージョンのID
        :param milestone_id: マイルストーンのID
        :param status_id: 状態のID
        :param priority_id: 優先度のID
        :param assignee_id: 担当者のID
        :param created_user_id: 登録者のID
        :param resolution_id: 完了理由のID
        :param parent_child: 親子課題の 0:すべて, 1:子課題以外, 2:子課題, 3:親課題でも子課題でもない課題, 4:親課題
        :param attachment: 添付ファイルを含む場合はtrue
        :param shared_file: 共有ファイルを含む場合はtrue
        :param sort: 課題一覧のソートに使用する属性名
        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param offset: オフセット
        :param count: 取得上限(1-100)  指定が無い場合は20
        :param created_since: 登録日 (yyyy-MM-dd)
        :param created_until: 登録日 (yyyy-MM-dd)
        :param updated_since: 更新日 (yyyy-MM-dd)
        :param updated_until: 更新日 (yyyy-MM-dd)
        :param start_date_since: 開始日 (yyyy-MM-dd)
        :param start_date_until: 開始日 (yyyy-MM-dd)
        :param due_date_since: 期限日 (yyyy-MM-dd)
        :param due_date_until: 期限日 (yyyy-MM-dd)
        :param id_: 課題のID
        :param parent_issue_id: 親課題のID
        :param keyword: 検索キーワード
        :param custom_field_text: カスタム属性(テキスト)の検索キーワード  e.g.) {1: 'debug', 2: 'top'}
        :param custom_field_num: カスタム属性(数値)の最小・最大値  e.g.) {1: {'min': 10, 'max': 20}, 2: {'min': None, 'max': 100}}
        :param custom_field_date: カスタム属性(日付)の最小・最大値  e.g.) {1: {'min': '2000-01-01', max: '2000-12-31'}}
        :param custom_field_list: カスタム属性(リスト)の指定ID  e.g.) {1: [100, 101, 102], 2: [200]}
        :return: レスポンス
        """

        path = self.base_path + '/count'

        payloads = {}
        if project_id is not None:
            payloads['projectId[]'] = project_id
        if issue_type_id is not None:
            payloads['issueTypeId[]'] = issue_type_id
        if category_id is not None:
            payloads['categoryId[]'] = category_id
        if version_id is not None:
            payloads['versionId[]'] = version_id
        if milestone_id is not None:
            payloads['milestoneId[]'] = milestone_id
        if status_id is not None:
            payloads['statusId[]'] = status_id
        if priority_id is not None:
            payloads['priorityId[]'] = priority_id
        if assignee_id is not None:
            payloads['assigneeId[]'] = assignee_id
        if created_user_id is not None:
            payloads['createdUserId[]'] = created_user_id
        if resolution_id is not None:
            payloads['resolutionId[]'] = resolution_id
        if parent_child is not None:
            payloads['parentChild'] = parent_child
        if attachment is not None:
            payloads['attachment'] = attachment
        if shared_file is not None:
            payloads['sharedFile'] = shared_file
        if sort is not None:
            payloads['sort'] = sort
        if order is not None:
            if order not in {'desc', 'asc'}:
                raise ValueError('order は desc または asc のみが使用できます')
            payloads['order'] = order
        if offset is not None:
            payloads['offset'] = offset
        if count is not None:
            if not 1 <= count <= 100:
                raise ValueError('count(取得上限)は1-100の範囲で指定してください')
        if created_since is not None:
            payloads['createdSince'] = created_since
        if created_until is not None:
            payloads['createdUntil'] = created_until
        if updated_since is not None:
            payloads['updatedSince'] = updated_since
        if updated_until is not None:
            payloads['updatedUntil'] = updated_until
        if start_date_since is not None:
            payloads['startDateSince'] = start_date_since
        if start_date_until is not None:
            payloads['startDateUntil'] = start_date_until
        if due_date_since is not None:
            payloads['dueDateSince'] = due_date_since
        if due_date_until is not None:
            payloads['dueDateUntil'] = due_date_until
        if id_ is not None:
            payloads['id[]'] = id_
        if parent_issue_id is not None:
            payloads['parentIssueId[]'] = parent_issue_id
        if keyword is not None:
            payloads['keyword'] = keyword
        if custom_field_text is not None:
            for field_id in custom_field_text:
                payloads['customField_{field_id}'.format(field_id=field_id)] = custom_field_text[field_id]
        if custom_field_num is not None:
            for field_id in custom_field_num:
                if custom_field_num[field_id]['min']:
                    payloads['customField_{field_id}_min'.format(field_id=field_id)] = custom_field_num[field_id]['min']
                if custom_field_num[field_id]['max']:
                    payloads['customField_{field_id}_max'.format(field_id=field_id)] = custom_field_num[field_id]['max']
        if custom_field_date is not None:
            for field_id in custom_field_date:
                if custom_field_date[field_id]['min']:
                    payloads['customField_{field_id}_min'.format(field_id=field_id)] = custom_field_date[field_id][
                        'min']
                if custom_field_date[field_id]['max']:
                    payloads['customField_{field_id}_max'.format(field_id=field_id)] = custom_field_date[field_id][
                        'max']
        if custom_field_list is not None:
            for field_id in custom_field_list:
                payloads['customField_{field_id}[]'.format(field_id=field_id)] = custom_field_list[field_id]

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_issue(self,
                  issue_id_or_key: str,
                  ) -> Response:
        """
        課題情報の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-issue/

        :param issue_id_or_key: 課題のID または 課題キー

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}'.format(issue_id_or_key=issue_id_or_key)

        return self.rs.send_get_request(path=path, url_param={})

    def add_issue(self,
                  project_id: int,
                  summary: str,
                  issue_type_id: int,
                  priority_id: int,
                  parent_issue_id: Optional[int] = None,
                  description: Optional[str] = None,
                  start_date: Optional[str] = None,
                  due_date: Optional[str] = None,
                  estimated_hours: Optional[int] = None,
                  actual_hours: Optional[int] = None,
                  category_id: Optional[List[int]] = None,
                  version_id: Optional[List[int]] = None,
                  milestone_id: Optional[List[int]] = None,
                  assignee_id: Optional[int] = None,
                  notified_user_id:
                  List[int] = None,
                  attachment_id: Optional[List[int]] = None,
                  **kwargs,
                  ) -> Response:
        """
        課題の追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-issue/

        :param project_id: 課題を登録するプロジェクトのID
        :param summary: 課題の件名
        :param issue_type_id: 課題の種別のID
        :param priority_id: 課題の優先度のID
        :param parent_issue_id: 課題の親課題のID
        :param description: 課題の詳細
        :param start_date: 課題の開始日 (yyyy-MM-dd)
        :param due_date: 課題の期限日 (yyyy-MM-dd)
        :param estimated_hours: 課題の予定時間
        :param actual_hours: 課題の実績時間
        :param category_id: 課題のカテゴリーのID
        :param version_id: 課題の発生バージョンのID
        :param milestone_id: 課題のマイルストーンのID
        :param assignee_id: 課題の担当者のID
        :param notified_user_id: 課題の登録の通知を受け取るユーザーのID
        :param attachment_id: 添付ファイルの送信APIが返すID
        :param kwargs: カスタム属性を渡す customField_{id}=[value] または customField_{id}_otherValue=[value] の形式

        :return: レスポンス
        """

        path = self.base_path
        payloads = {}
        if project_id is not None:
            payloads['projectId'] = project_id
        if summary is not None:
            payloads['summary'] = summary
        if issue_type_id is not None:
            payloads['issueTypeId'] = issue_type_id
        if priority_id is not None:
            payloads['priorityId'] = priority_id
        if parent_issue_id is not None:
            payloads['parentIssueId'] = parent_issue_id
        if description is not None:
            payloads['description'] = description
        if start_date is not None:
            payloads['startDate'] = start_date
        if due_date is not None:
            payloads['dueDate'] = due_date
        if estimated_hours is not None:
            payloads['estimatedHours'] = estimated_hours
        if actual_hours is not None:
            payloads['actualHours'] = actual_hours
        if category_id is not None:
            payloads['categoryId[]'] = category_id
        if version_id is not None:
            payloads['versionId[]'] = version_id
        if milestone_id is not None:
            payloads['milestoneId[]'] = milestone_id
        if assignee_id is not None:
            payloads['assigneeId'] = assignee_id
        if notified_user_id is not None:
            payloads['notifiedUserId[]'] = notified_user_id
        if attachment_id is not None:
            payloads['attachmentId[]'] = attachment_id
        for key in kwargs:
            if re.match('^customField_[0-9]+_other_value$|^customField_[0-9]+$', key) is None:
                raise ValueError('カスタム属性の指定方法が正しくありません')
            payloads[key] = kwargs[key]

        return self.rs.send_post_request(path=path, request_param=payloads)

    def update_issue(self,
                     issue_id_or_key: str,
                     summary: Optional[str] = None,
                     parent_issue_id: Optional[int] = None,
                     description: Optional[str] = None,
                     status_id: Optional[int] = None,
                     resolution_id: Optional[int] = None,
                     start_date: Optional[str] = None,
                     due_date: Optional[str] = None,
                     estimated_hours: Optional[int] = None,
                     actual_hours: Optional[int] = None,
                     issue_type_id: Optional[int] = None,
                     category_id: Optional[List[int]] = None,
                     version_id: Optional[List[int]] = None,
                     milestone_id: Optional[List[int]] = None,
                     priority_id: Optional[int] = None,
                     assignee_id: Optional[int] = None,
                     notified_user_id: Optional[List[int]] = None,
                     attachment_id: Optional[List[int]] = None,
                     comment: Optional[str] = None,
                     **kwargs,
                     ) -> Response:
        """
        課題情報の更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-issue/

        :param issue_id_or_key: 課題のID または 課題キー
        :param summary: 課題の件名
        :param parent_issue_id: 課題の親課題のID
        :param description: 課題の詳細
        :param status_id: 状態のID
        :param resolution_id: 完了理由のID
        :param start_date: 課題の開始日 (yyyy-MM-dd)
        :param due_date: 課題の期限日 (yyyy-MM-dd)
        :param estimated_hours: 課題の予定時間
        :param actual_hours: 課題の実績時間
        :param issue_type_id: 課題の種別のID
        :param category_id: 課題のカテゴリーのID
        :param version_id: 課題の発生バージョンのID
        :param milestone_id: 課題のマイルストーンのID
        :param priority_id: 課題の優先度のID
        :param assignee_id: 課題の担当者のID
        :param notified_user_id: 課題の登録の通知を受け取るユーザーのID
        :param attachment_id: 添付ファイルの送信APIが返すID
        :param comment: コメント
        :param kwargs: カスタム属性を渡す customField_{id}=[value] または customField_{id}_otherValue=[value] の形式

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}'.format(issue_id_or_key=issue_id_or_key)
        payloads = {}
        if summary is not None:
            payloads['summary'] = summary
        if parent_issue_id is not None:
            payloads['parentIssueId'] = parent_issue_id
        if description is not None:
            payloads['description'] = description
        if status_id is not None:
            payloads['statusId'] = status_id
        if resolution_id is not None:
            payloads['resolutionId'] = resolution_id
        if start_date is not None:
            payloads['startDate'] = start_date
        if due_date is not None:
            payloads['dueDate'] = due_date
        if estimated_hours is not None:
            payloads['estimatedHours'] = estimated_hours
        if actual_hours is not None:
            payloads['actualHours'] = actual_hours
        if issue_type_id is not None:
            payloads['issueTypeId'] = issue_type_id
        if category_id is not None:
            payloads['categoryId[]'] = category_id
        if version_id is not None:
            payloads['versionId[]'] = version_id
        if milestone_id is not None:
            payloads['milestoneId[]'] = milestone_id
        if priority_id is not None:
            payloads['priorityId'] = priority_id
        if assignee_id is not None:
            payloads['assigneeId'] = assignee_id
        if notified_user_id is not None:
            payloads['notifiedUserId[]'] = notified_user_id
        if attachment_id is not None:
            payloads['attachmentId[]'] = attachment_id
        if comment is not None:
            payloads['comment'] = comment
        for key in kwargs:
            if re.match('^customField_[0-9]+_other_value$|^customField_[0-9]+$', key) is None:
                raise ValueError('カスタム属性の指定方法が正しくありません')
            payloads[key] = kwargs[key]

        return self.rs.send_patch_request(path=path, request_param=payloads)

    def delete_issue(self,
                     issue_id_or_key: str,
                     ) -> Response:
        """
        課題の削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-issue/

        :param issue_id_or_key: 課題のID または 課題キー

        :return: レスポンス
        """
        path = self.base_path + '/{issue_id_or_key}'.format(issue_id_or_key=issue_id_or_key)

        return self.rs.send_delete_request(path=path, request_param={})


class IssueAttachment:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'issues'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_list_of_issue_attachments(self,
                                      issue_id_or_key: str,
                                      ) -> Response:
        """
        課題添付ファイル一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-issue-attachments/

        :param issue_id_or_key: 課題のID または 課題キー

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/attachments'.format(issue_id_or_key=issue_id_or_key)

        return self.rs.send_get_request(path=path, url_param={})

    def get_issue_attachment(self,
                             issue_id_or_key: str,
                             attachment_id: int,
                             ) -> Tuple[str, Response]:
        """
        課題添付ファイルのダウンロード
        https://developer.nulab.com/ja/docs/backlog/api/2/get-issue-attachment/

        :param issue_id_or_key: 課題のID または 課題キー
        :param attachment_id: 添付ファイルのID

        :return: 保存されたファイルのPATH
        """

        path = self.base_path + '/{issue_id_or_key}/attachments/{attachment_id}' \
            .format(issue_id_or_key=issue_id_or_key, attachment_id=attachment_id)
        return self.rs.get_file(path, {})

    def delete_issue_attachment(self,
                                issue_id_or_key: str,
                                attachment_id: int,
                                ) -> Response:
        """
        課題添付ファイルの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-issue-attachment/

        :param issue_id_or_key: 課題のID または 課題キー
        :param attachment_id: 添付ファイルのID

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/attachments/{attachment_id}' \
            .format(issue_id_or_key=issue_id_or_key, attachment_id=attachment_id)

        return self.rs.send_delete_request(path=path, request_param={})


class IssueComment:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'issues'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_comment_list(self,
                         issue_id_or_key: Optional[str] = None,
                         min_id: Optional[int] = None,
                         max_id: Optional[int] = None,
                         count: int = 20,
                         order: str = 'desc',
                         ) -> Response:
        """
        課題コメントの取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-comment-list/

        :param issue_id_or_key: 課題のID または 課題キー
        :param min_id: 最小ID
        :param max_id: 最大ID
        :param count: 取得上限(1-100) 指定が無い場合は20
        :param order: “asc”または”desc” 指定が無い場合は”desc”

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/comments'.format(issue_id_or_key=issue_id_or_key)
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

    def add_comment(self,
                    issue_id_or_key: str,
                    content: str,
                    notified_user_id: Optional[List[int]] = None,
                    attachment_id: Optional[List[int]] = None,
                    ) -> Response:
        """
        課題コメントの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-comment/

        :param issue_id_or_key: 課題のID または 課題キー
        :param content: コメントの本文
        :param notified_user_id: コメント登録の通知を受け取るユーザーID
        :param attachment_id: 添付ファイルの送信APIが返すID

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/comments'.format(issue_id_or_key=issue_id_or_key)
        payloads = {'content': content}
        if notified_user_id is not None:
            payloads['notifiedUserId[]'] = notified_user_id
        if attachment_id is not None:
            payloads['attachmentId[]'] = attachment_id

        return self.rs.send_post_request(path=path, request_param=payloads)

    def get_comment(self,
                    issue_id_or_key: str,
                    comment_id: int,
                    ) -> Response:
        """
        課題コメント情報の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-comment/

        :param issue_id_or_key: 課題のID または 課題キー
        :param comment_id: コメントのID

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/comments/{comment_id}' \
            .format(issue_id_or_key=issue_id_or_key, comment_id=comment_id)

        return self.rs.send_get_request(path=path, url_param={})

    def update_comment(self,
                       issue_id_or_key: str,
                       comment_id: int,
                       content: Optional[str] = None,
                       ) -> Response:
        """
        課題コメント情報の更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-comment/

        :param issue_id_or_key: 課題のID または 課題キー
        :param comment_id: コメントのID
        :param content: コメントの本文

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/comments/{comment_id}' \
            .format(issue_id_or_key=issue_id_or_key, comment_id=comment_id)
        payloads = {}
        if content is not None:
            payloads['content'] = content

        return self.rs.send_patch_request(path=path, request_param=payloads)

    def get_list_of_comment_notifications(self,
                                          issue_id_or_key: str,
                                          comment_id: int,
                                          ) -> Response:
        """
        課題コメントのお知らせ一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-comment-notifications/

        :param issue_id_or_key: 課題のID または 課題キー
        :param comment_id: コメントのID

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/comments/{comment_id}/notifications' \
            .format(issue_id_or_key=issue_id_or_key, comment_id=comment_id)

        return self.rs.send_get_request(path=path, url_param={})

    def delete_comment(self,
                       issue_id_or_key: str,
                       comment_id: int,
                       ) -> Response:
        """
        課題コメントの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-comment/

        :param issue_id_or_key: 課題のID または 課題キー
        :param comment_id: コメントのID

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/comments/{comment_id}' \
            .format(issue_id_or_key=issue_id_or_key, comment_id=comment_id)

        return self.rs.send_delete_request(path=path, request_param={})

    def count_comment(self,
                      issue_id_or_key: str,
                      ) -> Response:
        """
        課題コメント数の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/count-comment/

        :param issue_id_or_key: 課題のID または 課題キー

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/comments/count'.format(issue_id_or_key=issue_id_or_key)

        return self.rs.send_get_request(path=path, url_param={})

    def add_comment_notification(self,
                                 issue_id_or_key: str,
                                 comment_id: int,
                                 notified_user_id: Optional[List[int]] = None,
                                 ) -> Response:
        """
        課題コメントにお知らせを追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-comment-notification/

        :param issue_id_or_key: 課題のID または 課題キー
        :param comment_id: コメントのID
        :param notified_user_id: 課題の登録の通知を受け取るユーザーのID

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/comments/{comment_id}/notifications' \
            .format(issue_id_or_key=issue_id_or_key, comment_id=comment_id)
        payloads = {}
        if notified_user_id is not None:
            payloads['notifiedUserId[]'] = notified_user_id

        return self.rs.send_post_request(path=path, request_param=payloads)


class IssueSharedFile:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'issues'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_list_of_linked_shared_files(self,
                                        issue_id_or_key: str,
                                        ) -> Response:
        """
        課題共有ファイル一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-linked-shared-files/

        :param issue_id_or_key: 課題のID または 課題キー

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/sharedFiles/'.format(issue_id_or_key=issue_id_or_key)

        return self.rs.send_get_request(path=path, url_param={})

    def remove_link_to_shared_file_from_issue(self,
                                              issue_id_or_key: str,
                                              shared_file_id: int,
                                              ) -> Response:
        """
        課題の共有ファイルのリンクを解除
        https://developer.nulab.com/ja/docs/backlog/api/2/remove-link-to-shared-file-from-issue/

        :param issue_id_or_key: 課題のID または 課題キー
        :param shared_file_id: 共有ファイルのID

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/sharedFiles/{shared_file_id}' \
            .format(issue_id_or_key=issue_id_or_key, shared_file_id=shared_file_id)

        return self.rs.send_delete_request(path=path, request_param={})

    def link_shared_files_to_issue(self,
                                   issue_id_or_key: str,
                                   file_id: List[int]
                                   ) -> Response:
        """
        課題に共有ファイルをリンク
        https://developer.nulab.com/ja/docs/backlog/api/2/link-shared-files-to-issue/

        :param issue_id_or_key: 課題のID または 課題キー
        :param file_id: 共有ファイルのID

        :return: レスポンス
        """

        path = self.base_path + '/{issue_id_or_key}/sharedFiles/'.format(issue_id_or_key=issue_id_or_key)
        payloads = {'fileId[]': file_id}

        return self.rs.send_post_request(path=path, request_param=payloads)


class IssueType:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_issue_type_list(self,
                            project_id_or_key: str) -> Response:
        """
        種別一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-issue-type-list/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/issueTypes'.format(project_id_or_key=project_id_or_key)
        return self.rs.send_get_request(path=path, url_param={})

    def update_issue_type(self,
                          project_id_or_key: str,
                          issue_id: int,
                          name: Optional[str] = None,
                          color: Optional[str] = None) -> Response:
        """
        種別情報の更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-issue-type/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param issue_id: 種別のID
        :param name: 種別の名前
        :param color: 種別の背景色

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/issueTypes/{issue_id}' \
            .format(project_id_or_key=project_id_or_key, issue_id=issue_id)
        payloads = {}
        if name is not None:
            payloads['name'] = name
        if color is not None:
            payloads['color'] = color

        return self.rs.send_patch_request(path=path, request_param=payloads)

    def add_issue_type(self,
                       project_id_or_key: Optional[str] = None,
                       name: Optional[str] = None,
                       color: Optional[str] = None) -> Response:
        """
        種別の追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-issue-type/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param name: 種別の名前
        :param color: 種別の背景色：以下から指定”#e30000””#990000””#934981””#814fbc””#2779ca””#007e9a””#7ea800””#ff9200””#ff3265””#666665”

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/issueTypes'.format(project_id_or_key=project_id_or_key)
        payloads = {}
        if name is not None:
            payloads['name'] = name
        if color is not None:
            payloads['color'] = color

        return self.rs.send_post_request(path=path, request_param=payloads)

    def delete_issue_type(self,
                          project_id_or_key: Optional[str] = None,
                          issue_id: Optional[int] = None,
                          substitute_issue_type_id: Optional[int] = None) -> Response:
        """
        種別の削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-issue-type/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param issue_id: 種別のID
        :param substitute_issue_type_id: 紐づく課題を付け替える先の種別のID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/issueTypes/{issue_id}' \
            .format(project_id_or_key=project_id_or_key, issue_id=issue_id)
        payloads = {}
        if substitute_issue_type_id is not None:
            payloads['substituteIssueTypeId'] = substitute_issue_type_id

        return self.rs.send_delete_request(path=path, request_param=payloads)
