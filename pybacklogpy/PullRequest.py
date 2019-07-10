from typing import List, Optional, Tuple

from requests import Response

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class PullRequest:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_number_of_pull_requests(self,
                                    project_id_or_key: str,
                                    repo_id_or_name: str,
                                    status_id: Optional[List[int]] = None,
                                    assignee_id: Optional[List[int]] = None,
                                    issue_id: Optional[List[int]] = None,
                                    created_user_id: Optional[List[int]] = None,
                                    offset: Optional[int] = None,
                                    count: Optional[int] = 20,
                                    ) -> Response:

        """
        プルリクエスト数の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-number-of-pull-requests/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param status_id: 状態のID
        :param assignee_id: 担当者のID
        :param issue_id: 関連課題のID
        :param created_user_id: 登録者のID
        :param offset:
        :param count: 取得上限(1-100)  指定が無い場合は20

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/pullRequests/count'\
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name)
        payloads = {}
        if status_id is not None:
            payloads['statusId[]'] = status_id
        if assignee_id is not None:
            payloads['assigneeId[]'] = assignee_id
        if issue_id is not None:
            payloads['issueId[]'] = issue_id
        if created_user_id is not None:
            payloads['createdUserId[]'] = created_user_id
        if offset is not None:
            payloads['offset'] = offset
        if count is not None:
            if not 1 <= count <= 100:
                raise ValueError('count(取得上限)は1-100の範囲で指定してください')

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_pull_request_list(self,
                              project_id_or_key: str,
                              repo_id_or_name: str,
                              status_id: Optional[List[int]] = None,
                              assignee_id: Optional[List[int]] = None,
                              issue_id: Optional[List[int]] = None,
                              created_user_id: Optional[List[int]] = None,
                              offset: Optional[int] = None,
                              count: int = 20,
                              ) -> Response:

        """
        プルリクエスト一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-pull-request-list/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param status_id: 状態のID
        :param assignee_id: 担当者のID
        :param issue_id: 関連課題のID
        :param created_user_id: 登録者のID
        :param offset:
        :param count: 取得上限(1-100)  指定が無い場合は20

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/pullRequests/' \
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name)
        payloads = {}
        if status_id is not None:
            payloads['statusId[]'] = status_id
        if assignee_id is not None:
            payloads['assigneeId[]'] = assignee_id
        if issue_id is not None:
            payloads['issueId[]'] = issue_id
        if created_user_id is not None:
            payloads['createdUserId[]'] = created_user_id
        if offset is not None:
            payloads['offset'] = offset
        if count is not None:
            if not 1 <= count <= 100:
                raise ValueError('count(取得上限)は1-100の範囲で指定してください')

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_pull_request(self,
                         project_id_or_key: str,
                         repo_id_or_name: str,
                         number: int,
                         ) -> Response:

        """
        プルリクエストの取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-pull-request/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param number: プルリクエストの番号

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/pullRequests/{number}' \
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name, number=number)

        return self.rs.send_get_request(path=path, url_param={})

    def add_pull_request(self,
                         project_id_or_key: str,
                         repo_id_or_name: str,
                         summary: str,
                         description: str,
                         base: str,
                         branch: str,
                         issue_id: Optional[int] = None,
                         assignee_id: Optional[int] = None,
                         notified_user_id: Optional[List[int]] = None,
                         attachment_id:
                         List[int] = None,
                         ) -> Response:

        """
        プルリクエストの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-pull-request/
        
        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param summary: プルリクエストの件名
        :param description: プルリクエストの詳細
        :param base: マージ先のブランチ名
        :param branch: マージされるブランチ名
        :param issue_id: 関連課題のID
        :param assignee_id: プルリクエストの担当者のID
        :param notified_user_id: プルリクエストの登録の通知を受け取るユーザーのID
        :param attachment_id: 添付ファイルの送信APIが返すID
        
        :return: レスポンス
        """
        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/pullRequests/' \
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name)
        payloads = {'summary': summary, 'description': description, 'base': base, 'branch': branch}
        if issue_id is not None:
            payloads['issueId'] = issue_id
        if assignee_id is not None:
            payloads['assigneeId'] = assignee_id
        if notified_user_id is not None:
            payloads['notifiedUserId[]'] = notified_user_id
        if attachment_id is not None:
            payloads['attachmentId[]'] = attachment_id

        return self.rs.send_post_request(path=path, request_param=payloads)

    def update_pull_request(self,
                            project_id_or_key: str,
                            repo_id_or_name: str,
                            number: int,
                            summary: Optional[str] = None,
                            description: Optional[str] = None,
                            issue_id: Optional[int] = None,
                            assignee_id: Optional[int] = None,
                            notified_user_id: Optional[List[int]] = None,
                            comment: Optional[str] = None,
                            ) -> Response:

        """
        プルリクエストの更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-pull-request/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param number: プルリクエストの番号
        :param summary: プルリクエストの件名
        :param description: プルリクエストの詳細
        :param issue_id: 関連課題のID
        :param assignee_id: プルリクエストの担当者のID
        :param notified_user_id: プルリクエストの登録の通知を受け取るユーザーのID
        :param comment: コメント

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/pullRequests/{number}' \
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name, number=number)
        payloads = {}
        if summary is not None:
            payloads['summary'] = summary
        if description is not None:
            payloads['description'] = description
        if issue_id is not None:
            payloads['issueId'] = issue_id
        if assignee_id is not None:
            payloads['assigneeId'] = assignee_id
        if notified_user_id is not None:
            payloads['notifiedUserId[]'] = notified_user_id
        if comment is not None:
            payloads['comment'] = comment

        return self.rs.send_patch_request(path=path, request_param=payloads)


class PullRequestAttachment:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_list_of_pull_request_attachment(self,
                                            project_id_or_key: str,
                                            repo_id_or_name: str,
                                            number: int,
                                            ) -> Response:

        """
        プルリクエスト添付ファイル一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-pull-request-attachment/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param number: プルリクエストの番号

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/' \
                                'pullRequests/{number}/attachments' \
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name, number=number)

        return self.rs.send_get_request(path=path, url_param={})

    def download_pull_request_attachment(self,
                                         project_id_or_key: str,
                                         repo_id_or_name: str,
                                         number: int,
                                         attachment_id: int,
                                         ) -> Tuple[str, Response]:

        """
        プルリクエスト添付ファイルのダウンロード
        https://developer.nulab.com/ja/docs/backlog/api/2/download-pull-request-attachment/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param number: プルリクエストの番号
        :param attachment_id: 添付ファイルのID

        :return: ダウンロードされたファイルのPATH
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/' \
                                'pullRequests/{number}/attachments/{attachment_id}' \
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name,
                    number=number, attachment_id=attachment_id)

        return self.rs.get_file(path=path, url_param={})

    def delete_pull_request_attachments(self,
                                        project_id_or_key: str,
                                        repo_id_or_name: str,
                                        number: int,
                                        attachment_id: int,
                                        ) -> Response:

        """
        プルリクエスト添付ファイルの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-pull-request-attachments/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param number: プルリクエストの番号
        :param attachment_id: 添付ファイルのID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/' \
                                'pullRequests/{number}/attachments/{attachment_id}' \
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name,
                    number=number, attachment_id=attachment_id)

        return self.rs.send_delete_request(path=path, request_param={})


class PullRequestComment:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'projects'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_pull_request_comment(self,
                                 project_id_or_key: str,
                                 repo_id_or_name: str,
                                 number: Optional[int] = None,
                                 min_id: Optional[int] = None,
                                 max_id: Optional[int] = None,
                                 count: int = 20,
                                 order: str = 'desc',
                                 ) -> Response:

        """
        プルリクエストコメントの取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-pull-request-comment/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param number: プルリクエストの番号
        :param min_id: 最小ID
        :param max_id: 最大ID
        :param count: 取得上限(1-100) 指定が無い場合は20
        :param order: “asc”または”desc” 指定が無い場合は”desc”

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/pullRequests/{number}/comments'\
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name, number=number)
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

    def add_pull_request_comment(self,
                                 project_id_or_key: str,
                                 repo_id_or_name: str,
                                 number: int,
                                 content: str,
                                 notified_user_id: Optional[List[int]] = None,
                                 ) -> Response:

        """
        プルリクエストコメントの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-pull-request-comment/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param number: プルリクエストの番号
        :param content: コメントの本文
        :param notified_user_id: コメント登録の通知を受け取るユーザーID

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/pullRequests/{number}/comments'\
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name, number=number)
        payloads = {'content': content}
        if notified_user_id is not None:
            payloads['notifiedUserId[]'] = notified_user_id

        return self.rs.send_post_request(path=path, request_param=payloads)

    def get_number_of_pull_request_comments(self,
                                            project_id_or_key: str,
                                            repo_id_or_name: str,
                                            number: int,
                                            ) -> Response:

        """
        プルリクエストコメント数の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-number-of-pull-request-comments/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param number: プルリクエストの番号

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/' \
                                'pullRequests/{number}/comments/count' \
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name, number=number)

        return self.rs.send_get_request(path=path, url_param={})

    def update_pull_request_comment_information(self,
                                                project_id_or_key: str,
                                                repo_id_or_name: str,
                                                number: int,
                                                comment_id: int,
                                                content: Optional[str] = None,
                                                ) -> Response:

        """
        プルリクエストコメント情報の更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-pull-request-comment-information/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param repo_id_or_name: リポジトリのID または リポジトリ名
        :param number: プルリクエストの番号
        :param comment_id: コメントのID
        :param content: コメントの本文

        :return: レスポンス
        """

        path = self.base_path + '/{project_id_or_key}/git/repositories/{repo_id_or_name}/' \
                                'pullRequests/{number}/comments/{comment_id}' \
            .format(project_id_or_key=project_id_or_key, repo_id_or_name=repo_id_or_name,
                    number=number, comment_id=comment_id)
        payloads = {}
        if content is not None:
            payloads['content'] = content

        return self.rs.send_patch_request(path=path, request_param=payloads)
