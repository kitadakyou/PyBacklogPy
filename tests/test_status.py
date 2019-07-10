import unittest

from pybacklogpy.Status import Status
from tests.utils import response_to_json


class TestStatus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # プロジェクト ID を取得、存在しなければ作成する
        cls.status = Status()

    def test_get_status_list(self):
        response = self.status.get_status_list()
        self.assertTrue(response.ok, msg='状態一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='状態一覧の取得に失敗')


if __name__ == '__main__':
    unittest.main()
