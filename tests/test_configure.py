import unittest

from pybacklogpy.BacklogConfigure import BacklogComConfigure
from pybacklogpy.Issue import Issue


class Test(unittest.TestCase):
    def test_config_and_get_issues(self):
        config = BacklogComConfigure(space_id='kitadakyou',
                                     api_key='dummy_api_key')

        issue = Issue(config)
        self.assertTrue(True, msg='プログラムからのspaceid, apikey の設定に失敗')
        response = issue.get_issue_list()
        self.assertTrue(response.ok, msg='プログラムから設定した場合、課題一覧の取得に失敗')


if __name__ == '__main__':
    unittest.main()
