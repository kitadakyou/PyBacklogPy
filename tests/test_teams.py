import unittest

from pybacklogpy.Team import Team
from tests.utils import response_to_json


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.team = Team()

    def test_get_list_of_teams(self):
        with self.assertRaises(ValueError, msg='チーム一覧取得時、orderのバリデーションに失敗'):
            self.team.get_list_of_teams(
                order='aaa',
            )
        with self.assertRaises(ValueError, msg='チーム一覧取得時、countのバリデーションに失敗'):
            self.team.get_list_of_teams(
                count=10000,
            )
        response = self.team.get_list_of_teams(
            order='asc',
            count=1,
        )
        self.assertTrue(response.ok, msg='チーム一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='チーム一覧の取得に失敗')


if __name__ == '__main__':
    unittest.main()
