import os
from time import sleep
import unittest

from pybacklogpy.Project import Project
from tests.utils import get_project_id_and_key, response_to_json


class TestProject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # プロジェクト ID を取得、存在しなければ作成する
        cls.project = Project()
        cls.project_id, cls.project_key = get_project_id_and_key()

    def setUp(self):
        rj = response_to_json(self.project.get_project_list())
        self.project_id = rj[0]['id']
        self.project_key = rj[0]['projectKey']

    # def test_delete_and_create_project(self):
    #     now = datetime.now()
    #     response_delete = self.project.delete_project(project_id_or_key=str(self.project_id))
    #     self.assertTrue(response_delete.ok, msg='プロジェクトの削除に失敗')
    #     sleep(10)  # 即時に実行すると key の重複エラーになる
    #
    #     with self.assertRaises(ValueError, msg='プロジェクト追加時、キーのバリデーションに失敗'):
    #         self.project.add_project(
    #             name='test_{YYYYMMDD}'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #             key='ERROR KEY!!!'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #             chart_enabled=False,
    #             project_leader_can_edit_project_leader=True,
    #             subtasking_enabled=False,
    #             text_formatting_rule='markdown'
    #         )
    #     with self.assertRaises(ValueError, msg='プロジェクト追加時、テキスト整形のルールのバリデーションに失敗'):
    #         self.project.add_project(
    #             name='test_{YYYYMMDD}'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #             key='TEST_PROJECT_{YYYYMMDD}'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #             chart_enabled=False,
    #             project_leader_can_edit_project_leader=True,
    #             subtasking_enabled=False,
    #             text_formatting_rule='wrong_format'
    #         )
    #     response_post = self.project.add_project(
    #         name='test_{YYYYMMDD}'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #         key='TEST_PROJECT_{YYYYMMDD}'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #         chart_enabled=False,
    #         project_leader_can_edit_project_leader=True,
    #         subtasking_enabled=False,
    #         text_formatting_rule='markdown'
    #     )
    #     self.assertTrue(response_post.ok, msg='プロジェクトの追加に失敗')
    #     response_post_dict = response_to_json(response_post)
    #     self.assertEqual(response_post_dict['name'], 'test_{YYYYMMDD}'
    #                      .format(YYYYMMDD=now.strftime('%Y%m%d')), msg='プロジェクトの登録情報が不正')
    #     self.assertEqual(response_post_dict['projectKey'], 'TEST_PROJECT_{YYYYMMDD}'
    #                      .format(YYYYMMDD=now.strftime('%Y%m%d')), msg='プロジェクトの登録情報が不正')
    #     self.assertEqual(response_post_dict['chartEnabled'], False, msg='プロジェクトの登録情報が不正')
    #     self.assertEqual(response_post_dict['projectLeaderCanEditProjectLeader'], True, msg='プロジェクトの登録情報が不正')
    #     self.assertEqual(response_post_dict['subtaskingEnabled'], False, msg='プロジェクトの登録情報が不正')
    #     self.assertEqual(response_post_dict['textFormattingRule'], 'markdown', msg='プロジェクトの登録情報が不正')
    #     self.project_id = response_post_dict['id']
    #
    #     response_get = self.project.get_project(project_id_or_key=str(self.project_id))
    #     self.assertTrue(response_get.ok, msg='プロジェクト情報の取得に失敗')
    #     response_get_dict = response_to_json(response_get)
    #     self.assertEqual(response_get_dict['name'], 'test_{YYYYMMDD}'
    #                      .format(YYYYMMDD=now.strftime('%Y%m%d')), msg='プロジェクトの登録情報が不正')
    #     self.assertEqual(response_get_dict['projectKey'], 'TEST_PROJECT_{YYYYMMDD}'
    #                      .format(YYYYMMDD=now.strftime('%Y%m%d')), msg='プロジェクトの登録情報が不正')
    #     self.assertEqual(response_get_dict['chartEnabled'], False, msg='プロジェクトの登録情報が不正')
    #     self.assertEqual(response_get_dict['projectLeaderCanEditProjectLeader'], True, msg='プロジェクトの登録情報が不正')
    #     self.assertEqual(response_get_dict['subtaskingEnabled'], False, msg='プロジェクトの登録情報が不正')
    #     self.assertEqual(response_get_dict['textFormattingRule'], 'markdown', msg='プロジェクトの登録情報が不正')
    #
    # def test_update_project(self):
    #     now = datetime.now()
    #
    #     with self.assertRaises(ValueError, msg='プロジェクト更新時、キーのバリデーションに失敗'):
    #         self.project.update_project(
    #             project_id_or_key=str(self.project_id),
    #             name='test_{YYYYMMDD}'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #             key='ERROR KEY!!!'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #             chart_enabled=False,
    #             project_leader_can_edit_project_leader=True,
    #             subtasking_enabled=False,
    #             text_formatting_rule='markdown'
    #         )
    #     with self.assertRaises(ValueError, msg='プロジェクト更新時、テキスト整形のルールのバリデーションに失敗'):
    #         self.project.update_project(
    #             project_id_or_key=str(self.project_id),
    #             name='test_{YYYYMMDD}'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #             key='TEST_PROJECT_{YYYYMMDD}'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #             chart_enabled=False,
    #             project_leader_can_edit_project_leader=True,
    #             subtasking_enabled=False,
    #             text_formatting_rule='wrong_format',
    #             archived=True,
    #         )
    #     response_update = self.project.update_project(
    #         project_id_or_key=str(self.project_id),
    #         name='test2_{YYYYMMDD}'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #         key='TEST_PROJECT_2_{YYYYMMDD}'.format(YYYYMMDD=now.strftime('%Y%m%d')),
    #         chart_enabled=False,
    #         project_leader_can_edit_project_leader=False,
    #         subtasking_enabled=False,
    #         text_formatting_rule='backlog',
    #         archived=True,
    #     )
    #     self.assertTrue(response_update.ok, msg='プロジェクトの更新に失敗')
    #     response_update_dict = response_to_json(response_update)
    #     self.assertEqual(response_update_dict['name'], 'test2_{YYYYMMDD}'
    #                      .format(YYYYMMDD=now.strftime('%Y%m%d')), msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_update_dict['projectKey'], 'TEST_PROJECT_2_{YYYYMMDD}'
    #                      .format(YYYYMMDD=now.strftime('%Y%m%d')), msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_update_dict['chartEnabled'], False, msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_update_dict['projectLeaderCanEditProjectLeader'], False, msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_update_dict['subtaskingEnabled'], False, msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_update_dict['textFormattingRule'], 'backlog', msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_update_dict['archived'], True, msg='プロジェクトの更新情報が不正')
    #
    #     response_get = self.project.get_project(project_id_or_key=str(self.project_id))
    #     self.assertTrue(response_get.ok, msg='プロジェクト情報の取得に失敗')
    #     response_get_dict = response_to_json(response_get)
    #     self.assertEqual(response_get_dict['name'], 'test2_{YYYYMMDD}'
    #                      .format(YYYYMMDD=now.strftime('%Y%m%d')), msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_get_dict['projectKey'], 'TEST_PROJECT_2_{YYYYMMDD}'
    #                      .format(YYYYMMDD=now.strftime('%Y%m%d')), msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_get_dict['chartEnabled'], False, msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_get_dict['projectLeaderCanEditProjectLeader'], False, msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_get_dict['subtaskingEnabled'], False, msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_get_dict['textFormattingRule'], 'backlog', msg='プロジェクトの更新情報が不正')
    #     self.assertEqual(response_get_dict['archived'], True, msg='プロジェクトの更新情報が不正')

    def test_get_project_list(self):
        response = self.project.get_project_list()
        self.assertTrue(response.ok, msg='プロジェクト一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='プロジェクト一覧の取得に失敗')
        self.assertNotEqual(response_list, [], msg='プロジェクト一覧の取得に失敗')

    def test_get_project_icon(self):
        file_path, response = self.project.get_project_icon(
            project_id_or_key=str(self.project_id),
        )
        self.assertTrue(file_path, msg='プロジェクトアイコンの取得に失敗')
        self.assertIsInstance(file_path, str, msg='プロジェクトアイコンの取得に失敗')
        self.assertTrue(os.path.exists(file_path), msg='プロジェクトアイコンの取得に失敗(ファイルが存在しない)')

    def test_get_project_recent_updates(self):
        with self.assertRaises(ValueError, msg='プロジェクト活動状況の取得時、取得上限のルールのバリデーションに失敗'):
            self.project.get_project_recent_updates(
                project_id_or_key=str(self.project_id),
                count=0,
                order='asc',
            )
        with self.assertRaises(ValueError, msg='プロジェクト活動状況の取得時、並び順のルールのバリデーションに失敗'):
            self.project.get_project_recent_updates(
                project_id_or_key=str(self.project_id),
                count=10,
                order='abc',
            )
        response = self.project.get_project_recent_updates(
            project_id_or_key=str(self.project_id),
            count=10,
            order='asc',
        )
        self.assertTrue(response.ok, msg='プロジェクト活動状況の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, (list, dict), msg='プロジェクト活動状況の取得に失敗')


if __name__ == '__main__':
    unittest.main()
