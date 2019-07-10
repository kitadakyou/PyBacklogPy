import unittest

from pybacklogpy.Version import Version
from tests.data import basic_version_data, updated_version_data
from tests.utils import get_project_id_and_key, response_to_json


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.version = Version()
        cls.project_id, cls.project_key = get_project_id_and_key()

    def test_get_version_milestone_list(self):
        response = self.version.get_version_milestone_list(
            project_id_or_key=self.project_key
        )
        self.assertTrue(response.ok, msg='バージョン(マイルストーン)一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='バージョン(マイルストーン)一覧の取得に失敗')

    def test_edit_version(self):
        version_num_before_add = len(response_to_json(self.version.get_version_milestone_list(
            project_id_or_key=self.project_key,
        )))

        response_post = self.version.add_version_milestone(
            project_id_or_key=self.project_key,
            name=basic_version_data['name'],
            description=basic_version_data['description'],
            start_date=basic_version_data['start_date'],
            release_due_date=basic_version_data['release_due_date']
        )
        self.assertTrue(response_post, msg='バージョンの追加に失敗')
        response_post_dict = response_to_json(response_post)
        self.assertIsInstance(response_post_dict, dict, msg='バージョン追加のレスポンスが辞書でない')
        version_id = response_post_dict['id']

        version_num_after_add = len(response_to_json(self.version.get_version_milestone_list(
            project_id_or_key=self.project_key,
        )))
        self.assertEqual(version_num_before_add + 1, version_num_after_add,
                         msg='バージョンを追加したにもかかわらず数が増えていない')

        response_patch = self.version.update_version_milestone(
            version_id=version_id,
            project_id_or_key=self.project_key,
            name=updated_version_data['name'],
            description=updated_version_data['description'],
            archived=updated_version_data['archived'],
            start_date=updated_version_data['start_date'],
            release_due_date=updated_version_data['release_due_date']
        )
        self.assertTrue(response_patch.ok, msg='バージョンの更新に失敗')
        response_patch_dict = response_to_json(response_patch)
        self.assertIsInstance(response_patch_dict, dict, msg='バージョン更新のレスポンスが辞書でない')

        response_delete = self.version.delete_version(
            project_id_or_key=self.project_key,
            version_id=version_id,
        )
        self.assertTrue(response_delete.ok, msg='バージョンの削除に失敗')

        version_num_after_delete = len(response_to_json(self.version.get_version_milestone_list(
            project_id_or_key=self.project_key,
        )))
        self.assertEqual(version_num_after_add - 1, version_num_after_delete,
                         msg='バージョンを削除したにもかかわらず数が減っていない')

if __name__ == '__main__':
    unittest.main()
