import unittest

from pybacklogpy.Resolution import Resolution
from tests.utils import response_to_json


class TestResolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resolution = Resolution()

    def test_get_resolution_list(self):
        response = self.resolution.get_resolution_list()
        self.assertTrue(response.ok, msg='完了理由一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='完了理由一覧の取得に失敗')


if __name__ == '__main__':
    unittest.main()
