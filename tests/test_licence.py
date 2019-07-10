import unittest

from pybacklogpy.Licence import Licence
from tests.utils import response_to_json


class TestLicence(unittest.TestCase):
    def test_get_license(self):
        licence = Licence()
        response = licence.get_licence()
        self.assertTrue(response.ok, msg='ライセンス情報の取得に失敗')
        response_dict = response_to_json(response)
        self.assertIsInstance(response_dict, dict, msg='ライセンス情報の取得に失敗')
        self.assertNotEqual(response_dict, [], msg='ライセンス情報の取得に失敗')


if __name__ == '__main__':
    unittest.main()
