from requests import Response
from typing import List, Optional, Tuple

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Wiki:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'wikis'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def update_wiki_page(self,
                         wiki_id: int,
                         name: Optional[str] = None,
                         content: Optional[str] = None,
                         mail_notify: bool = False,
                         ) -> Response:
        """
        Wikiページ情報の更新
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/update-wiki-page/

        :param wiki_id: WikiページのID
        :param name: ページ名
        :param content: ページの内容
        :param mail_notify: ページの更新をメールで通知する場合はtrue

        :return: レスポンス
        """
        path = self.base_path + '/{wiki_id}'.format(wiki_id=wiki_id)
        if not (name or content):
            ValueError('更新される内容がありません')
        payloads = {'mailNotify': mail_notify}
        if name is not None:
            payloads['name'] = name
        if content is not None:
            payloads['content'] = content

        return self.rs.send_patch_request(path=path, request_param=payloads)

    def get_wiki_page(self,
                      wiki_id: int,
                      ) -> Response:
        """
        Wikiページ情報の取得
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-wiki-page/

        :param wiki_id: WikiページのID
        :return: レスポンス
        """

        path = self.base_path + '/' + str(wiki_id)

        return self.rs.send_get_request(path=path)

    def add_wiki_page(self,
                      project_id: int,
                      name: str,
                      content: str,
                      mail_notify: Optional[bool] = None,
                      ) -> Response:
        """
        Wikiページの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-wiki-page/

        :param project_id: プロジェクトのID
        :param name: ページ名
        :param content: ページの内容
        :param mail_notify: ページの追加をメールで通知する場合はtrue

        :return: レスポンス
        """

        path = self.base_path
        payloads = {'projectId': project_id, 'name': name, 'content': content}
        if mail_notify is not None:
            payloads['mailNotify'] = mail_notify

        return self.rs.send_post_request(path=path, request_param=payloads)

    def delete_wiki_page(self,
                         wiki_id: int,
                         mail_notify: Optional[bool] = None,
                         ) -> Response:

        """
        Wikiページの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-wiki-page/

        :param wiki_id: WikiページのID
        :param mail_notify: ページの削除をメールで通知する場合はtrue

        :return: レスポンス
        """

        path = self.base_path + '/{wiki_id}'.format(wiki_id=wiki_id)
        payloads = {}
        if mail_notify is not None:
            payloads['mailNotify'] = mail_notify

        return self.rs.send_delete_request(path=path, request_param=payloads)

    def count_wiki_page(self,
                        project_id_or_key: str,
                        ) -> Response:

        """
        Wikiページ数の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/count-wiki-page/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/count'
        payloads = {}
        if project_id_or_key is not None:
            payloads['projectIdOrKey'] = project_id_or_key

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_wiki_page_list(self,
                           project_id_or_key: Optional[str] = None,
                           keyword: Optional[str] = None,
                           ) -> Response:

        """
        Wikiページ一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-wiki-page-list/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー
        :param keyword: 検索キーワード

        :return: レスポンス
        """

        path = self.base_path
        payloads = {}
        if project_id_or_key is not None:
            payloads['projectIdOrKey'] = project_id_or_key
        if keyword is not None:
            payloads['keyword'] = keyword

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_wiki_page_tag_list(self,
                               project_id_or_key: Optional[int] = None,
                               ) -> Response:

        """
        Wikiページタグ一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-wiki-page-tag-list/

        :param project_id_or_key: プロジェクトのID または プロジェクトキー

        :return: レスポンス
        """

        path = self.base_path + '/tags'
        payloads = {}
        if project_id_or_key is not None:
            payloads['projectIdOrKey'] = project_id_or_key

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_wiki_page_history(self,
                              wiki_id: Optional[int] = None,
                              min_id: Optional[int] = None,
                              max_id: Optional[int] = None,
                              count: int = 20,
                              order: str = 'desc',
                              ) -> Response:
        """
        Wikiページ更新履歴一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-wiki-page-history/

        :param wiki_id: WikiページのID
        :param min_id: 最小ID
        :param max_id: 最大ID
        :param count: 取得上限(1-100) 指定が無い場合は20
        :param order: “asc”または”desc” 指定が無い場合は”desc”

        :return: レスポンス
        """

        path = self.base_path + '/{wiki_id}/history'.format(wiki_id=str(wiki_id))
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

    def get_wiki_page_star(self,
                           wiki_id: Optional[int] = None,
                           ) -> Response:
        """
        Wikiページのスター一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-wiki-page-star/

        :param wiki_id: WikiページのID

        :return: レスポンス
        """

        path = self.base_path + '/{wiki_id}/stars'.format(wiki_id=str(wiki_id))

        return self.rs.send_get_request(path=path, url_param={})


class WikiAttachment:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'wikis'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def attach_file_to_wiki(self,
                            wiki_id: int,
                            attachment_id: Optional[List[int]] = None,
                            ) -> Response:
        """
        Wiki添付ファイルの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/attach-file-to-wiki/

        :param wiki_id: WikiページのID
        :param attachment_id: 添付ファイルの送信APIが返すID

        :return: レスポンス
        """

        path = self.base_path + '/{wiki_id}/attachments'.format(wiki_id=str(wiki_id))
        payloads = {}
        if attachment_id is not None:
            payloads['attachmentId[]'] = attachment_id

        return self.rs.send_post_request(path=path, request_param=payloads)

    def get_wiki_page_attachment(self,
                                 wiki_id: int,
                                 attachment_id: Optional[int] = None,
                                 ) -> Tuple[str, Response]:
        """
        Wiki添付ファイルのダウンロード
        https://developer.nulab.com/ja/docs/backlog/api/2/get-wiki-page-attachment/

        :param wiki_id: WikiページのID
        :param attachment_id: 添付ファイルのID

        :return: 保存されたファイルのPATH
        """

        path = self.base_path + '/{wiki_id}/attachments/{attachment_id}'\
            .format(wiki_id=str(wiki_id), attachment_id=attachment_id)

        return self.rs.get_file(path=path, url_param={})

    def get_list_of_wiki_attachments(self,
                                     wiki_id: int,
                                     ) -> Response:
        """
        Wiki添付ファイル一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-wiki-attachments/

        :param wiki_id: WikiページのID

        :return: レスポンス
        """

        path = self.base_path + '/{wiki_id}/attachments'.format(wiki_id=str(wiki_id))
        return self.rs.send_get_request(path=path, url_param={})

    def remove_wiki_attachment(self,
                               wiki_id: int,
                               attachment_id: Optional[int] = None,
                               ) -> Response:

        """
        Wiki添付ファイルの削除
        https://developer.nulab.com/ja/docs/backlog/api/2/remove-wiki-attachment/

        :param wiki_id: WikiページのID
        :param attachment_id: 添付ファイルのID

        :return: レスポンス
        """

        path = self.base_path + '/{wiki_id}/attachments/{attachment_id}'\
            .format(wiki_id=wiki_id, attachment_id=attachment_id)

        return self.rs.send_delete_request(path=path, request_param={})


class WikiSharedFile:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'wikis'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def get_list_of_shared_files_on_wiki(self,
                                         wiki_id: int,
                                         ) -> Response:

        """
        Wiki共有ファイル一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-list-of-shared-files-on-wiki/

        :param wiki_id: WikiページのID

        :return: レスポンス
        """

        path = self.base_path + '/{wiki_id}/sharedFiles'.format(wiki_id=str(wiki_id))

        return self.rs.send_get_request(path=path, url_param={})

    def link_shared_files_to_wiki(self,
                                  wiki_id: int,
                                  file_id: List[int],
                                  ) -> Response:
        """
        Wikiに共有ファイルをリンク
        https://developer.nulab.com/ja/docs/backlog/api/2/link-shared-files-to-wiki/

        :param wiki_id: WikiページのID
        :param file_id: 共有ファイルのID

        :return: レスポンス
        """

        path = self.base_path + '/{wiki_id}/sharedFiles'.format(wiki_id=str(wiki_id))
        payloads = {}
        if file_id is not None:
            payloads['fileId[]'] = file_id

        return self.rs.send_post_request(path=path, request_param=payloads)

    def remove_link_to_shared_file_from_wiki(self,
                                             wiki_id: int,
                                             file_id: int,
                                             ) -> Response:

        """
        Wikiの共有ファイルのリンクを解除
        https://developer.nulab.com/ja/docs/backlog/api/2/remove-link-to-shared-file-from-wiki/

        :param wiki_id: WikiページのID
        :param file_id: 共有ファイルのID

        :return: レスポンス
        """

        path = self.base_path + '/{wiki_id}/sharedFiles/{file_id}'.format(wiki_id=str(wiki_id), file_id=str(file_id))

        return self.rs.send_delete_request(path=path, request_param={})
