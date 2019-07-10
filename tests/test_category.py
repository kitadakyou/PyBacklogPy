from datetime import datetime
import unittest

from pybacklogpy.Category import Category
from tests.utils import get_project_id_and_key, response_to_json


class TestCategory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.category = Category()
        cls.project_id, cls.project_key = get_project_id_and_key()

# def test_add_category(self):
    #     now = datetime.now()
    #     category_name =
    #     response = self.category.add_category(
    #         project_id_or_key=self.project_key,
    #         name='test{YYYYMMDDHHMM}'.format(YYYYMMDDHHMM=now.strftime('%Y%m%d%H%M'))
    #     )
    #     response_json = response_to_json(response)
    #     self.assertTrue(response.ok, msg='カテゴリーの追加に失敗')

    def test_get_category_list(self):
        response = self.category.get_category_list(project_id_or_key=self.project_key)
        self.assertTrue(response.ok, msg='カテゴリー一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='カテゴリー一覧の取得に失敗')




if __name__ == '__main__':
    unittest.main()
