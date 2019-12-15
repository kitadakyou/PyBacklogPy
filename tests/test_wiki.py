from datetime import datetime
from os.path import exists
import unittest

from pybacklogpy.Attachment import Attachment
from pybacklogpy.Wiki import Wiki, WikiAttachment
from tests.utils import get_project_id_and_key, get_wiki_id, response_to_json
from tests.data import basic_wiki_data, get_YYYYMMDDHHMMSS_name, updated_wiki_data


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_id, cls.project_key = get_project_id_and_key()
        cls.wiki = Wiki()
        cls.wiki_attachment = WikiAttachment()
        cls.attachment = Attachment()

    def test_get_wiki_page_list(self):
        response = self.wiki.get_wiki_page_list(
            project_id_or_key=self.project_key,
        )
        self.assertTrue(response.ok, msg='Wikiページ一覧の取得に失敗')
        response_list = response_to_json(response)
        self.assertIsInstance(response_list, list, msg='Wikiページ一覧の取得に失敗')

    def test_add_wiki_page(self):
        wiki_page_count_before = response_to_json(self.wiki.count_wiki_page(self.project_key))['count']
        response_post = self.wiki.add_wiki_page(
            project_id=self.project_id,
            name=basic_wiki_data['name'],
            content=basic_wiki_data['content'],
            mail_notify=basic_wiki_data['mail_notify']
        )
        self.assertTrue(response_post.ok, msg='Wikiページの追加リクエストに失敗')
        wiki_page_count_after = response_to_json(self.wiki.count_wiki_page(self.project_key))['count']
        self.assertEqual(wiki_page_count_before + 1, wiki_page_count_after, '追加したにもかかわらずWikiページ数が増えていない')

    def test_update_wiki_page(self):
        now = datetime.now()
        wiki_id = get_wiki_id()
        response = self.wiki.update_wiki_page(
            wiki_id=wiki_id,
            name=updated_wiki_data['name'],
            content=updated_wiki_data['content'],
            mail_notify=updated_wiki_data['mail_notify'],
        )
        self.assertTrue(response.ok, msg='Wikiの更新に失敗')
        response_dict = response_to_json(response)
        self.assertEqual(response_dict['name'], updated_wiki_data['name'], msg='更新後のWikiタイトルが不正')
        self.assertEqual(response_dict['content'], updated_wiki_data['content'], msg='更新後のWiki本文が不正')
        response2 = self.wiki.update_wiki_page(
            wiki_id=wiki_id,
            name=get_YYYYMMDDHHMMSS_name('wiki_updated2', now),
            content=basic_wiki_data['content'],
            mail_notify=basic_wiki_data['mail_notify'],
        )
        self.assertTrue(response2.ok, msg='Wikiの2度目の更新に失敗')

    def test_delete_wiki_page(self):
        now = datetime.now()
        r = self.wiki.add_wiki_page(
                project_id=self.project_id,
                name=get_YYYYMMDDHHMMSS_name('wiki_to_delete', now),
                content=basic_wiki_data['content'],
                mail_notify=basic_wiki_data['mail_notify']
            )
        delete_wiki_id = response_to_json(r)['id']
        wiki_page_count_before = response_to_json(self.wiki.count_wiki_page(self.project_key))['count']
        response_delete = self.wiki.delete_wiki_page(
            wiki_id=delete_wiki_id
        )
        self.assertTrue(response_delete.ok, msg='Wikiの削除に失敗')
        wiki_page_count_after = response_to_json(self.wiki.count_wiki_page(self.project_key))['count']
        self.assertEqual(wiki_page_count_before - 1, wiki_page_count_after, '削除したにもかかわらずWikiページ数が減っていない')

    def test_get_wiki_page_tag_list(self):
        response_get = self.wiki.get_wiki_page_tag_list(
            project_id_or_key=self.project_id,
        )
        self.assertTrue(response_get.ok, msg='Wikiページタグ一覧の取得に失敗')
        response_list = response_to_json(response_get)
        self.assertIsInstance(response_list, list, msg='Wikiページタグ一覧がリストオブジェクトではない')

    def test_wiki_page_history(self):
        wiki_id = get_wiki_id()
        with self.assertRaises(ValueError, msg='Wikiページ更新履歴一覧の取得時、orderのバリデーションに失敗'):
            self.wiki.get_wiki_page_history(
                wiki_id=wiki_id,
                order='abc',
            )
        with self.assertRaises(ValueError, msg='Wikiページ更新履歴一覧の取得時、countのバリデーションに失敗'):
            self.wiki.get_wiki_page_history(
                wiki_id=wiki_id,
                count=0,
            )
        with self.assertRaises(ValueError, msg='Wikiページ更新履歴一覧の取得時、countのバリデーションに失敗'):
            self.wiki.get_wiki_page_history(
                wiki_id=wiki_id,
                count=101,
            )
        response_get = self.wiki.get_wiki_page_history(
            wiki_id=wiki_id,
            count=1,
            order='asc',
        )
        self.assertTrue(response_get.ok, msg='Wikiページ更新履歴一覧の取得に失敗')
        response_list = response_to_json(response_get)
        self.assertIsInstance(response_list, list, msg='Wikiページ更新履歴一覧がリストオブジェクトではない')

    def test_get_wiki_page_star(self):
        wiki_id = get_wiki_id()
        response_get = self.wiki.get_wiki_page_star(
            wiki_id=wiki_id,
        )
        self.assertTrue(response_get.ok, msg='Wikiページのスター一覧の取得に失敗')
        response_list = response_to_json(response_get)
        self.assertIsInstance(response_list, list, msg='Wikiページのスター一覧がリストオブジェクトではない')


    def test_attach_and_remove_file(self):
        from pybacklogpy.Licence import Licence
        _license = Licence()
        if response_to_json(_license.get_licence())['licenceTypeId'] == 11:
            self.skipTest(reason='無料版ライセンスだとWikiのファイル添付機能が使えない')

        now = datetime.now()
        wiki_id = get_wiki_id()
        response_send_file = self.attachment.post_attachment_file(
            filepath='tmp/150.png',
            filename=get_YYYYMMDDHHMMSS_name('image_', now) + '.png',
        )
        self.assertTrue(response_send_file.ok, msg='添付ファイルの送信に失敗')
        response_send_file_dict = response_to_json(response_send_file)
        self.assertIsInstance(response_send_file_dict, dict, msg='添付ファイルの送信のレスポンスが辞書でない')
        attachment_id = response_send_file_dict['id']

        attachments_num_before_post = len(response_to_json(self.wiki_attachment.get_list_of_wiki_attachments(wiki_id)))

        response_post = self.wiki_attachment.attach_file_to_wiki(
            wiki_id=wiki_id,
            attachment_id=[attachment_id],
        )
        self.assertTrue(response_post.ok, msg='Wiki添付ファイルの追加に失敗')
        response_post_list = response_to_json(response_post)
        self.assertIsInstance(response_post_list, list, msg='Wiki添付ファイルの追加のレスポンスがリストでない')

        attachments_num_after_post = len(response_to_json(self.wiki_attachment.get_list_of_wiki_attachments(wiki_id)))
        self.assertEqual(attachments_num_before_post + 1, attachments_num_after_post,
                         msg='Wiki添付ファイルの追加後にファイル数が増えていない')

        response_get = self.wiki_attachment.get_list_of_wiki_attachments(
            wiki_id=wiki_id,
        )
        self.assertTrue(response_get.ok, msg='Wiki添付ファイル一覧の取得に失敗')
        response_list = response_to_json(response_get)
        self.assertIsInstance(response_list, list, msg='Wiki添付ファイル一覧の取得がリストでない')
        wiki_attachment_id = response_list[0]['id']

        downloaded_file_path, response = self.wiki_attachment.get_wiki_page_attachment(
            wiki_id=wiki_id,
            attachment_id=wiki_attachment_id,
        )
        self.assertTrue(exists(downloaded_file_path), msg='ファイルのダウンロードに失敗')

        response_delete = self.wiki_attachment.remove_wiki_attachment(
            wiki_id=wiki_id,
            attachment_id=wiki_attachment_id,
        )
        self.assertTrue(response_delete.ok, msg='Wiki添付ファイルの削除に失敗')

        attachments_num_after_delete = len(response_to_json(self.wiki_attachment.get_list_of_wiki_attachments(wiki_id)))
        self.assertEqual(attachments_num_after_post - 1, attachments_num_after_delete,
                         msg='Wiki添付ファイルの削除後にファイル数が減っていない')


if __name__ == '__main__':
    unittest.main()
