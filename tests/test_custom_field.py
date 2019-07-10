from datetime import datetime
import unittest

from pybacklogpy.const import CUSTOM_FIELD_TYPE
from pybacklogpy.CustomField import CustomField
from tests.utils import get_project_id_and_key, response_to_json


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_id, cls.project_key = get_project_id_and_key()
        cls.custom_field = CustomField()

    def test_get_custom_field(self):
        from pybacklogpy.Licence import Licence
        l = Licence()
        if response_to_json(l.get_licence())['licenceTypeId'] == 11:
            self.skipTest(reason='無料版ライセンスだとカスタム属性の設定ができない')

        response = self.custom_field.get_custom_field_list(
            project_id_or_key=self.project_key
        )
        self.assertTrue(response.ok, msg='カスタム属性一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='カスタム属性一覧の取得に失敗')

    def test_add_custom_field(self):
        from pybacklogpy.Licence import Licence
        l = Licence()
        if response_to_json(l.get_licence())['licenceTypeId'] == 11:
            self.skipTest(reason='無料版ライセンスだとカスタム属性の設定ができない')

        now = datetime.now()
        response_list_field = self.custom_field.add_custom_field(
            project_id_or_key=self.project_key,
            type_id=CUSTOM_FIELD_TYPE['単一リスト'],
            name='test_custom_field_list_{YYMMDD}'.format(YYMMDD=now.strftime('%Y%m%d')),
            items=[
                '要素1',
                '要素2',
                '要素3',
            ],
            allow_input=True,
            allow_add_item=True,
        )
        self.assertTrue(response_list_field.ok, msg='単一リストカスタム属性の追加に失敗')
        list_field_id = response_to_json(response_list_field)['id']

        response_string_field = self.custom_field.add_custom_field(
            project_id_or_key=self.project_key,
            type_id=CUSTOM_FIELD_TYPE['文字列'],
            name='test_custom_field_string_{YYMMDD}'.format(YYMMDD=now.strftime('%Y%m%d')),
        )
        self.assertTrue(response_string_field.ok, msg='文字列カスタム属性の追加に失敗')
        string_field_id = response_to_json(response_string_field)['id']

        response_number_filed = self.custom_field.add_custom_field(
            project_id_or_key=self.project_key,
            type_id=CUSTOM_FIELD_TYPE['数値'],
            name='test_custom_field_number_{YYMMDD}'.format(YYMMDD=now.strftime('%Y%m%d')),
            min_num=0,
            max_num=100,
            initial_value=50,
            unit='人月'
        )
        self.assertTrue(response_number_filed.ok, msg='数値カスタム属性の追加に失敗')
        number_field_id = response_to_json(response_number_filed)['id']

        response_date_field = self.custom_field.add_custom_field(
            project_id_or_key=self.project_key,
            type_id=CUSTOM_FIELD_TYPE['日付'],
            name='test_custom_field_date_{YYMMDD}'.format(YYMMDD=now.strftime('%Y%m%d')),
            min_date='2016-01-01',
            max_date='2020-12-31',
        )
        self.assertTrue(response_date_field.ok, msg='日付カスタム属性の追加に失敗')


if __name__ == '__main__':
    unittest.main()
