import unittest

from pybacklogpy.Priority import Priority
from tests.utils import response_to_json


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.priority = Priority()

    def test_get_priority_list(self):
        response = self.priority.get_priority_list()
        self.assertTrue(response.ok, msg='優先度一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='優先度一覧の取得に失敗')


if __name__ == '__main__':
    unittest.main()
