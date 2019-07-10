from os.path import exists
import unittest

from pybacklogpy.const import ACTIVITY_TYPE
from pybacklogpy.User import User
from tests.utils import get_myself_user_id, response_to_json


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User()
        cls.myself_user_id = get_myself_user_id()

    def test_get_user_list(self):
        user = User()
        response = user.get_user_list()
        self.assertTrue(response.ok, msg='ユーザー一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='ユーザー一覧の取得に失敗')
        self.assertNotEqual(response_list, [], msg='ユーザー一覧の取得に失敗')

    def test_get_own_user(self):
        response = self.user.get_own_user()
        self.assertTrue(response.ok, msg='認証ユーザー情報の取得に失敗')
        response_dict = response_to_json(response)
        self.assertIsInstance(response_dict, dict, msg='認証ユーザー情報のレスポンスが辞書でない')

    def test_get_user_icon(self):
        user_id = self.myself_user_id
        filepath, response = self.user.get_user_icon(
            user_id=user_id
        )
        self.assertTrue(response.ok, msg='ユーザーアイコンのダウンロードに失敗')
        self.assertTrue(exists(filepath), msg='ユーザーアイコンがダウンロードされていない')

    def test_get_user_recent_updates(self):
        user_id = self.myself_user_id
        with self.assertRaises(ValueError, msg='ユーザーの最近の活動取得時、取得上限のルールのバリデーションに失敗'):
            self.user.get_user_recent_updates(
                user_id=user_id,
                count=0,
            )
        with self.assertRaises(ValueError, msg='ユーザーの最近の活動取得時、取得上限のルールのバリデーションに失敗'):
            self.user.get_user_recent_updates(
                user_id=user_id,
                order='abc',
            )
        with self.assertRaises(ValueError, msg='ユーザーの最近の活動取得時、activity_type_idのバリデーションに失敗'):
            self.user.get_user_recent_updates(
                user_id=user_id,
                activity_type_id=[0],
            )
        with self.assertRaises(ValueError, msg='ユーザーの最近の活動取得時、activity_type_idのバリデーションに失敗'):
            self.user.get_user_recent_updates(
                user_id=user_id,
                activity_type_id=[1, 2, 3, 18],
            )
        response = self.user.get_user_recent_updates(
            user_id=user_id,
            activity_type_id=[ACTIVITY_TYPE['課題の追加']],
            min_id=1,
            count=10,
            order='asc',
        )
        self.assertTrue(response.ok, msg='ユーザーの最近の活動取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='ユーザーの最近の活動取得のレスポンスがリストでない')

    def test_count_user_received_stars(self):
        user_id = self.myself_user_id

        with self.assertRaises(ValueError, msg='ユーザーが受け取ったスター数の取得のsinceのバリデーションに失敗'):
            self.user.count_user_received_stars(
                user_id=user_id,
                since='2019-1-1'
            )
        with self.assertRaises(ValueError, msg='ユーザーが受け取ったスター数の取得のuntilのバリデーションに失敗'):
            self.user.count_user_received_stars(
                user_id=user_id,
                until='2019/01/01'
            )
        response = self.user.count_user_received_stars(
            user_id=user_id,
            since='2000-01-01',
            until='2099-12-31'
        )
        self.assertTrue(response.ok, msg='ユーザーの受け取ったスターの数の取得に失敗')
        response_dict = response_to_json(response)
        self.assertIsInstance(response_dict, dict, msg='ユーザーの受け取ったスターの数のレスポンスが辞書でない')

    def test_get_received_star_list(self):
        user_id = self.myself_user_id
        with self.assertRaises(ValueError, msg='ユーザーの受け取ったスター一覧の取得時、取得上限のルールのバリデーションに失敗'):
            self.user.get_received_star_list(
                user_id=user_id,
                count=0,
            )
        with self.assertRaises(ValueError, msg='ユーザーの受け取ったスター一覧の取得時、取得順序のルールのバリデーションに失敗'):
            self.user.get_received_star_list(
                user_id=user_id,
                order='abc',
            )
        response = self.user.get_received_star_list(
            user_id=user_id,
            min_id=1,
            count=2,
            order='asc',
        )
        self.assertTrue(response.ok, msg='ユーザーの受け取ったスター一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, (list, dict), msg='ユーザーの受け取ったスター一覧の取得のレスポンスが不正')

    def test_get_list_of_recently_viewed_issues(self):
        with self.assertRaises(ValueError, msg='自分が最近見た課題一覧の取得時、取得上限のルールのバリデーションに失敗'):
            self.user.get_list_of_recently_viewed_issues(
                count=0,
            )
        with self.assertRaises(ValueError, msg='自分が最近見た課題一覧の取得時、取得順序のルールのバリデーションに失敗'):
            self.user.get_list_of_recently_viewed_issues(
                order='abc',
            )
        response = self.user.get_list_of_recently_viewed_issues(
            count=2,
            offset=0,
            order='asc',
        )
        self.assertTrue(response.ok, msg='自分が最近見た課題一覧の取得時')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, (list, dict), msg='自分が最近見た課題一覧の取得のレスポンス形式が不正')

    def test_get_list_of_recently_viewed_projects(self):
        with self.assertRaises(ValueError, msg='自分が最近見たプロジェクト一覧の取得時、取得上限のルールのバリデーションに失敗'):
            self.user.get_list_of_recently_viewed_projects(
                count=0,
            )
        with self.assertRaises(ValueError, msg='自分が最近見たプロジェクト一覧の取得時、取得順序のルールのバリデーションに失敗'):
            self.user.get_list_of_recently_viewed_projects(
                order='abc',
            )
        response = self.user.get_list_of_recently_viewed_projects(
            count=2,
            offset=0,
            order='asc',
        )
        self.assertTrue(response.ok, msg='自分が最近見たプロジェクト一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, (list, dict), msg='自分が最近見たプロジェクト一覧の取得のレスポンス形式が不正')

    def test_get_list_of_recently_viewed_wikis(self):
        with self.assertRaises(ValueError, msg='自分が最近見たWiki一覧の取得時、取得上限のルールのバリデーションに失敗'):
            self.user.get_list_of_recently_viewed_wikis(
                count=0,
            )
        with self.assertRaises(ValueError, msg='自分が最近見たWiki一覧の取得時、取得順序のルールのバリデーションに失敗'):
            self.user.get_list_of_recently_viewed_wikis(
                order='abc',
            )
        response = self.user.get_list_of_recently_viewed_wikis(
            count=2,
            offset=0,
            order='asc',
        )
        self.assertTrue(response.ok, msg='自分が最近見たWiki一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, (list, dict), msg='自分が最近見たWiki一覧の取得のレスポンス形式が不正')


if __name__ == '__main__':
    unittest.main()
