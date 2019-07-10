from datetime import datetime
import json
from requests import Response
from typing import List, Tuple, Union


from pybacklogpy.Issue import Issue
from pybacklogpy.Project import Project
from pybacklogpy.User import User
from pybacklogpy.Wiki import Wiki
from tests import data


def get_myself_user_id() -> int:
    user = User()
    return int(response_to_json(user.get_own_user())['id'])


def get_project_id_and_key() -> Tuple[int, str]:
    """
    与えられたユーザーのスペースにあるプロジェクトIDとKeyを1つだけ返す。
    ない場合、作成する

    :return: project_id: int, project_key: str
    """
    project = Project()
    response_project_list = project.get_project_list()
    response_project_list_list = response_to_json(response_project_list)
    if response_project_list_list:
        project_id = response_project_list_list[0]['id']
        project_key = response_project_list_list[0]['projectKey']
    else:
        now = datetime.now()
        response = project.add_project(
            name='test_{YYYYMMDDHHMM}'.format(YYYYMMDDHHMM=now.strftime('%Y%m%d%H%M')),
            key='TEST_PROJECT_{YYYYMMDDHHMM}'.format(YYYYMMDDHHMM=now.strftime('%Y%m%d%H%M')),
            chart_enabled=False,
            project_leader_can_edit_project_leader=True,
            subtasking_enabled=False,
            text_formatting_rule='markdown'
        )
        project_id = response_to_json(response)['id']
        project_key = response_to_json(response)['projectKey']

    return project_id, project_key


def get_issue_id_and_key() -> Tuple[int, str]:
    issue = Issue()
    issue_list = response_to_json(issue.get_issue_list())
    if issue_list:
        issue = issue_list[0]
        return int(issue['id']), issue['issueKey']


def get_wiki_id() -> int:
    wiki = Wiki()
    project_id, project_key = get_project_id_and_key()
    wiki_list = response_to_json(wiki.get_wiki_page_list(project_id_or_key=project_key))
    if wiki_list and len(wiki_list) >= 2:
        return wiki_list[1]['id']
    r = wiki.add_wiki_page(
        project_id=project_id,
        name=data.basic_wiki_data['name'],
        content=data.basic_wiki_data['content'],
        mail_notify=data.basic_wiki_data['mail_notify'],
    )
    return response_to_json(r)['id']


def get_user_id() -> int:
    user = User()
    return response_to_json(user.get_user_list())[0]['id']


def response_to_json(r: Response) -> Union[dict, List[dict]]:
    """
    Requestモジュールの Response オブジェクトを受け取り、Json に変換して返す
    :param r: Response オブジェクト
    :return: List または Dict オブジェクト
    """
    return json.loads(r.text)
