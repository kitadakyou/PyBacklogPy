from typing import Optional

from requests import Response

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Project:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'stars'
        _config = config if config else None
        self.rs = RequestSender(_config)

    def add_star(self,
                 issue_id: Optional[int] = None,
                 comment_id: Optional[int] = None,
                 wiki_id: Optional[int] = None,
                 pull_request_id: Optional[int] = None,
                 pull_request_comment_id: Optional[int] = None,
                 ) -> Response:
        """
        スターの追加
        https://developer.nulab.com/ja/docs/backlog/api/2/add-star/

        :param issue_id: 課題のID
        :param comment_id: コメントのID
        :param wiki_id: WikiページのID
        :param pull_request_id: プルリクエストのID
        :param pull_request_comment_id: プルリクエストコメントのID

        :return: レスポンス
        """

        path = self.base_path
        payloads = {}
        if issue_id is not None:
            payloads['issueId'] = issue_id
        if comment_id is not None:
            payloads['commentId'] = comment_id
        if wiki_id is not None:
            payloads['wikiId'] = wiki_id
        if pull_request_id is not None:
            payloads['pullRequestId'] = pull_request_id
        if pull_request_comment_id is not None:
            payloads['pullRequestCommentId'] = pull_request_comment_id

        if not payloads:
            raise ValueError('スターを付ける対象が指定されていません')
        if not len(payloads) == 1:
            raise ValueError('一度のリクエストで追加出来るスターは1つだけです')

        return self.rs.send_get_request(path=path, url_param=payloads)
