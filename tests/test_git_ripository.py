import unittest

from pybacklogpy.GitRepository import GitRepository
from tests.utils import get_project_id_and_key, response_to_json


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.git_repository = GitRepository()
        cls.project_id, cls.project_key = get_project_id_and_key()

    def test_get_list_of_git_repositories(self):
        response = self.git_repository.get_list_of_git_repositories(
            project_id_or_key=self.project_key
        )
        self.assertTrue(response.ok, msg='Gitリポジトリ一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='Gitリポジトリ一覧の取得に失敗')




if __name__ == '__main__':
    unittest.main()
