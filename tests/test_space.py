from os.path import exists
import unittest

from pybacklogpy.Space import Space
from tests.utils import response_to_json


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.space = Space()

    def test_get_space(self):
        response = self.space.get_space()
        self.assertTrue(response.ok, msg='スペース情報の取得に失敗')
        response_dict = response_to_json(response)
        self.assertIsInstance(response_dict, dict, msg='スペース情報の取得に失敗')
        self.assertNotEqual(response_dict, {}, msg='スペース情報の取得に失敗')
        
    def test_get_recent_updates(self):
        with self.assertRaises(ValueError, msg='最近の更新の取得時、orderのバリデーションに失敗'):
            self.space.get_recent_updates(
                order='abc',
            )
        with self.assertRaises(ValueError, msg='最近の更新の取得時、countのバリデーションに失敗'):
            self.space.get_recent_updates(
                count=0,
            )
        with self.assertRaises(ValueError, msg='最近の更新の取得時、countのバリデーションに失敗'):
            self.space.get_recent_updates(
                count=101,
            )
        response = self.space.get_recent_updates(
            activity_type_id=[i for i in range(1, 27)],
            min_id=1,
            count=2,
            order='asc',
        )
        self.assertTrue(response.ok, msg='最近の更新の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='最近の更新のレスポンスがリストでない')

    def test_get_space_logo(self):
        path, response = self.space.get_space_logo()
        self.assertTrue(response.ok, msg='スペースロゴの取得に失敗')
        self.assertTrue(exists(path), msg='スペースロゴがダウンロードされていない')

    def test_get_space_notification(self):
        response = self.space.get_space_notification()
        self.assertTrue(response.ok, msg='スペースのお知らせの取得に失敗')
        response_dict = response_to_json(response)
        self.assertIsInstance(response_dict, dict, msg='スペースのお知らせ取得のレスポンスが辞書でない')

    def test_get_space_disk_usage(self):
        response = self.space.get_space_disk_usage()
        self.assertTrue(response.ok, msg='スペースの容量使用状況の取得に失敗')
        response_dict = response_to_json(response)
        self.assertIsInstance(response_dict, dict, msg='スペースの容量使用状況取得のレスポンスが辞書でない')

    # def test_update_space_notification(self):
    #     response = self.space.update_space_notification()
    #     self.assertTrue(response.ok, msg='スペースお知らせの更新に失敗')


if __name__ == '__main__':
    unittest.main()
