import unittest

from pybacklogpy.Webhook import Webhook
from tests.data import basic_webhook_data, updated_webhook_data
from tests.utils import get_project_id_and_key, response_to_json



class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.webhook = Webhook()
        cls.project_id, cls.project_key = get_project_id_and_key()

    def test_get_list_of_webhook(self):
        # Key
        response = self.webhook.get_list_of_webhooks(
            project_id_or_key=self.project_key
        )
        self.assertTrue(response.ok, msg='Webhook一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='Webhook一覧の取得に失敗')

        # ID
        response = self.webhook.get_list_of_webhooks(
            project_id_or_key=str(self.project_id)
        )
        self.assertTrue(response.ok, msg='Webhook一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='Webhook一覧の取得に失敗')

    def test_edit_webhook(self):
        webhook_num_before_add = len(response_to_json(
            self.webhook.get_list_of_webhooks(project_id_or_key=self.project_key),
        ))

        response_post = self.webhook.add_webhook(
            project_id_or_key=self.project_key,
            name=basic_webhook_data['name'],
            description=basic_webhook_data['description'],
            hook_url=basic_webhook_data['hook_url'],
            all_event=basic_webhook_data['all_event'],
            activity_type_ids=basic_webhook_data['activity_type_ids'],
        )
        self.assertTrue(response_post.ok, msg='Webhookの追加に失敗')
        response_post_dict = response_to_json(response_post)
        self.assertIsInstance(response_post_dict, dict, msg='Webhook追加のレスポンスが辞書でない')
        webhook_id = response_post_dict['id']

        webhook_num_after_add = len(response_to_json(
            self.webhook.get_list_of_webhooks(project_id_or_key=self.project_key),
        ))
        self.assertEqual(webhook_num_before_add + 1, webhook_num_after_add, msg='Webhookを追加したにもかかわらず数が増えていない')

        response_patch = self.webhook.update_webhook(
            project_id_or_key=self.project_key,
            webhook_id=webhook_id,
            name=updated_webhook_data['name'],
            description=updated_webhook_data['description'],
            hook_url=updated_webhook_data['hook_url'],
            all_event=updated_webhook_data['all_event'],
            activity_type_ids=updated_webhook_data['activity_type_ids'],
        )
        self.assertTrue(response_patch.ok, msg='Webhookの更新に失敗')
        response_patch_dict = response_to_json(response_patch)
        self.assertIsInstance(response_patch_dict, dict, msg='Webhook更新のレスポンスが辞書でない')

        response_get = self.webhook.get_webhook(
            project_id_or_key=self.project_key,
            webhook_id=webhook_id,
        )
        self.assertTrue(response_get.ok, msg='Webhookの取得に失敗')
        response_get_dict = response_to_json(response_get)
        self.assertIsInstance(response_get_dict, dict, msg='Webhook取得のレスポンスが辞書でない')
        self.assertEqual(response_get_dict['name'], updated_webhook_data['name'],
                         msg='Webhook の名前が正しく更新されていない')
        self.assertEqual(response_get_dict['description'], updated_webhook_data['description'],
                         msg='Webhook の詳細が正しく更新されていない')
        self.assertEqual(response_get_dict['activityTypeIds'], updated_webhook_data['activity_type_ids'],
                         msg='Webhook の通知するイベントIDが正しく更新されていない')

        response_delete = self.webhook.delete_webhook(
            project_id_or_key=self.project_key,
            webhook_id=webhook_id,
        )
        self.assertTrue(response_delete.ok, msg='Webhookの削除に失敗')

        webhook_num_after_delete = len(response_to_json(
            self.webhook.get_list_of_webhooks(project_id_or_key=self.project_key),
        ))
        self.assertEqual(webhook_num_after_add - 1, webhook_num_after_delete, msg='Webhookを削除したにもかかわらず数が減っていない')


if __name__ == '__main__':
    unittest.main()
