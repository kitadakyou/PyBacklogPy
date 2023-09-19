import unittest

from pybacklogpy.Status import Status
from tests.utils import get_project_id_and_key, response_to_json


class TestStatus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # プロジェクト ID を取得、存在しなければ作成する
        cls.project_id, cls.project_key = get_project_id_and_key()
        cls.status = Status()

    def test_status(self):
        from pybacklogpy.Licence import Licence
        l = Licence()
        if response_to_json(l.get_licence())['licenceTypeId'] == 11:
            self.skipTest(reason='無料版ライセンスだとカスタム状態の設定ができない')

        response_add_status = self.status.add_status(
            project_id_or_key=self.project_key,
            name='保留',
            color='#ea2c00',
        )
        self.assertTrue(response_add_status.ok, msg='状態の追加に失敗')
        status_id = response_to_json(response_add_status)['id']

        response_update_status = self.status.update_status(
            project_id_or_key=self.project_key,
            status_id=status_id,
            name='明日やる',
            color='#868cb7',
        )
        self.assertTrue(response_update_status.ok, msg='状態の更新に失敗')

        response_update_order = self.status.update_order_of_status(
            project_id_or_key=self.project_key,
            status_id=[1, 2, status_id, 3, 4],
        )
        self.assertTrue(response_update_order.ok, msg='状態の順序の更新に失敗')

        response_get_status_list = self.status.get_status_list(
            project_id_or_key=self.project_key
            )
        self.assertTrue(response_get_status_list.ok, msg='ステータス一覧の取得に失敗')
        response_list = response_to_json(response_get_status_list)
        self.assertIsInstance(response_list, list, msg='ステータス一覧の取得に失敗')
        
        response_delete_status = self.status.delete_status(
            project_id_or_key=self.project_key,
            status_id=status_id,
            substitute_status_id=1,
        )
        self.assertTrue(response_delete_status.ok, msg='状態の削除に失敗')


if __name__ == '__main__':
    unittest.main()
