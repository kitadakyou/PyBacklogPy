import unittest

from pybacklogpy.BacklogConfigure import BacklogComConfigure


class Test(unittest.TestCase):
    def test_config(self):
        _ = BacklogComConfigure(space_key='kitadakyou',
                                api_key='dummy_api_key')

        self.assertTrue(True, msg='プログラムからのspaceid, apikey の設定に失敗')


if __name__ == '__main__':
    unittest.main()
