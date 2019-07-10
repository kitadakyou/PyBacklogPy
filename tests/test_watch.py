import unittest

from pybacklogpy.Watch import Watch
from tests.data import basic_watching_data, updated_watching_data
from tests.utils import get_issue_id_and_key, get_myself_user_id, get_user_id, response_to_json


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.watch = Watch()
        cls.user_id = get_user_id()
        cls.issue_id, cls.issue_key = get_issue_id_and_key()

    def test_count_watching(self):
        response = self.watch.count_watching(
            user_id=self.user_id
        )
        self.assertTrue(response.ok, msg='完了理由一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, dict, msg='完了理由一覧の取得に失敗')

    def test_get_watching_list(self):
        with self.assertRaises(ValueError, msg='ウォッチ一覧の取得時、orderのバリデーションに失敗'):
            self.watch.get_watching_list(
                user_id=self.user_id,
                order='abc',
            )
        with self.assertRaises(ValueError, msg='ウォッチ一覧の取得時、countのバリデーションに失敗'):
            self.watch.get_watching_list(
                user_id=self.user_id,
                count=0,
            )
        with self.assertRaises(ValueError, msg='ウォッチ一覧の取得時、countのバリデーションに失敗'):
            self.watch.get_watching_list(
                user_id=self.user_id,
                count=101,
            )
        response_get = self.watch.get_watching_list(
            user_id=self.user_id,
            order='asc',
            count=2,
            offset=0,
            resource_already_read=False,
            issue_id=[self.issue_id]
        )
        self.assertTrue(response_get.ok, msg='ウォッチ一覧の取得に失敗')
        response_list = response_to_json(response_get)
        self.assertIsInstance(response_list, list, msg='ウォッチ一覧取得のレスポンスがリストでない')

    # def test_edit_watching(self):
    #     myself_user_id = get_myself_user_id()
    #     watching_num_before_add = response_to_json(self.watch.count_watching(
    #         user_id=myself_user_id,
    #         already_read=False,
    #     ))['count']
    #     self.assertIsInstance(watching_num_before_add, int, msg='ウォッチ数の取得に失敗')
    #
    #     response_post = self.watch.add_watching(
    #         issue_id_or_key=self.issue_key,
    #         note=basic_watching_data['note']
    #     )
    #     self.assertTrue(response_post.ok, msg='ウォッチの追加に失敗')
    #     response_post_dict = response_to_json(response_post)
    #     self.assertIsInstance(response_post_dict, dict, msg='ウォッチ追加のレスポンスが辞書でない')
    #     watch_id = response_post_dict['id']
    #
    #     response_patch = self.watch.update_watching(
    #         watching_id=watch_id,
    #         note=updated_watching_data['note']
    #     )
    #     self.assertTrue(response_patch.ok, msg='ウォッチの更新に失敗')
    #     response_patch_dict = response_to_json(response_patch)
    #     self.assertIsInstance(response_patch_dict, dict, msg='ウォッチ更新のレスポンスが辞書でない')
    #
    #     response_get = self.watch.get_watching(
    #         watching_id=watch_id
    #     )
    #     self.assertTrue(response_get.ok, msg='ウォッチの取得に失敗')
    #     response_get_dict = response_to_json(response_get)
    #     self.assertIsInstance(response_get_dict, dict, msg='ウォッチ取得のレスポンスが辞書でない')
    #     self.assertEqual(response_get_dict['note'], updated_watching_data['note'],
    #                      msg='ウォッチ の通知するイベントIDが正しく更新されていない')
    #
    #     response_delete = self.watch.delete_watching(
    #         watching_id=watch_id,
    #     )
    #     self.assertTrue(response_delete.ok, msg='ウォッチの削除に失敗')


if __name__ == '__main__':
    unittest.main()
