import unittest

from pybacklogpy.Issue import Issue, IssueType
from tests.data import basic_issue_data, updated_issue_data
from tests.utils import get_project_id_and_key, response_to_json


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.issue = Issue()
        cls.issue_type = IssueType()
        cls.project_id, cls.project_key = get_project_id_and_key()

    def test_get_issue_list(self):
        response = self.issue.get_issue_list()
        self.assertTrue(response.ok, msg='課題一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='課題一覧の取得に失敗')

    def test_issue_type(self):
        response_issue_list = self.issue_type.get_issue_type_list(
            project_id_or_key=self.project_key
        )
        self.assertTrue(response_issue_list.ok, msg='種別一覧の取得に失敗')
        issue_type_list = response_to_json(response_issue_list)
        self.assertIsInstance(issue_type_list, list, msg='課題追加のレスポンスがリストでない')

        issue_type_num_before_add = len(issue_type_list)

        response_delete = self.issue_type.delete_issue_type(
            project_id_or_key=self.project_key,
            issue_id=issue_type_list[3]['id'],
            substitute_issue_type_id=issue_type_list[0]['id']
        )
        self.assertTrue(response_delete.ok, msg='種別の削除に失敗')

        response_issue_list_2 = self.issue_type.get_issue_type_list(
            project_id_or_key=self.project_key
        )
        issue_type_list_2 = response_to_json(response_issue_list_2)
        issue_type_num_after_delete = len(issue_type_list_2)
        self.assertEqual(issue_type_num_before_add - 1, issue_type_num_after_delete,
                         '種別を削除したにもかかわらず課題数が減っていない')

        response_post = self.issue_type.add_issue_type(
            project_id_or_key=self.project_key,
            name='TEST',
            color='#e30000',
        )
        self.assertTrue(response_post.ok, msg='種別の種類追加に失敗')
        response_post_dict = response_to_json(response_post)
        self.assertIsInstance(response_post_dict, dict, msg='種別追加のレスポンスが辞書でない')
        issue_id = response_post_dict['id']

        response_issue_list_3 = self.issue_type.get_issue_type_list(
            project_id_or_key=self.project_key
        )
        issue_type_list_3 = response_to_json(response_issue_list_3)
        issue_type_num_after_add = len(issue_type_list_3)
        self.assertEqual(issue_type_num_after_delete + 1, issue_type_num_after_add,
                         '種別を追加したにもかかわらず数が増えていない')

        response_patch = self.issue_type.update_issue_type(
            project_id_or_key=self.project_key,
            issue_id=issue_id,
            name='その他',
            color='#2779ca',
        )
        self.assertTrue(response_patch.ok, msg='課題情報の更新に失敗')
        response_patch_dict = response_to_json(response_patch)
        self.assertIsInstance(response_patch_dict, dict, msg='種別更新のレスポンスが辞書でない')

    def test_edit_issue(self):
        response_issue_list = self.issue_type.get_issue_type_list(
            project_id_or_key=self.project_key
        )
        issue_type_list = response_to_json(response_issue_list)

        issue_num_before_add = response_to_json(self.issue.count_issue(
            project_id=[self.project_id],
        ))['count']

        response_post = self.issue.add_issue(
            project_id=self.project_id,
            summary=basic_issue_data['summary'],
            issue_type_id=issue_type_list[0]['id'],
            priority_id=basic_issue_data['priority_id'],
            description=basic_issue_data['description'],
            start_date=basic_issue_data['start_date'],
            due_date=basic_issue_data['due_date'],
        )
        self.assertTrue(response_post.ok, msg='課題の追加に失敗')
        response_post_dict = response_to_json(response_post)
        self.assertIsInstance(response_post_dict, dict, msg='課題追加のレスポンスが辞書でない')
        issue_key = response_post_dict['issueKey']

        issue_num_after_add = response_to_json(self.issue.count_issue(
            project_id=[self.project_id],
        ))['count']
        self.assertEqual(issue_num_before_add + 1, issue_num_after_add, msg='課題を追加したにも関わらず課題数が増えていない')

        response_patch = self.issue.update_issue(
            issue_id_or_key=str(issue_key),
            summary=updated_issue_data['summary'],
            issue_type_id=issue_type_list[1]['id'],
            priority_id=updated_issue_data['priority_id'],
            description=updated_issue_data['description'],
            start_date=updated_issue_data['start_date'],
            due_date=updated_issue_data['due_date'],
        )
        self.assertTrue(response_patch.ok, msg='課題の更新に失敗')
        response_patch_dict = response_to_json(response_patch)
        self.assertIsInstance(response_patch_dict, dict, msg='課題追加のレスポンスが辞書でない')

        response_delete = self.issue.delete_issue(
            issue_id_or_key=issue_key,
        )
        self.assertTrue(response_delete.ok, msg='課題の削除に失敗')

        issue_num_after_delete = response_to_json(self.issue.count_issue(
            project_id=[self.project_id],
        ))['count']
        self.assertEqual(issue_num_after_add - 1, issue_num_after_delete, msg='課題を削除したにも関わらず課題数が減っていない')


if __name__ == '__main__':
    unittest.main()
