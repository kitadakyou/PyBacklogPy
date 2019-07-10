import unittest

from pybacklogpy.Notification import Notification
from tests.utils import response_to_json


class TestNotification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notification = Notification()

    def test_get_notification(self):
        with self.assertRaises(ValueError, msg='お知らせ一覧の取得時、取得上限のルールのバリデーションに失敗'):
            self.notification.get_notification(
                count=0,
                order='asc',
            )
        with self.assertRaises(ValueError, msg='お知らせ一覧の取得時、取得上限のルールのバリデーションに失敗'):
            self.notification.get_notification(
                count=10,
                order='abc',
            )
        response = self.notification.get_notification(
            count=10,
            order='asc',
        )
        self.assertTrue(response.ok, msg='お知らせ一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, (list, dict), msg='お知らせ一覧の取得に失敗')


if __name__ == '__main__':
    unittest.main()
