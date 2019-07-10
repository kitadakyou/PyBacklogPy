import configparser
import requests
import re
from requests import Response
from typing import Optional, Tuple


from pybacklogpy.BacklogConfigure import BacklogConfigure


def convert_bool_to_str(request_param: dict) -> dict:
    """
    リクエストデータに bool の値があった場合、小文字のstr型に変える
    :param request_param:
    :return:
    """
    for key in request_param:
        if type(request_param[key]) == bool:
            request_param[key] = str(request_param[key]).lower()
    return request_param


class RequestSender:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        if config:  # プログラムから設定
            self.api_url = 'https://{backlog_host}/api/v2/'.format(backlog_host=config.api_url)
            self.api_key = config.api_key
        else:  # 設定ファイルから設定
            config_file = configparser.ConfigParser()
            config_file.read('secrets')
            self.api_url = 'https://{backlog_host}/api/v2/'.format(backlog_host=config_file['backlog']['Host'])
            self.api_key = config_file['backlog']['ApiKey']

        # 共通パラメーター
        self.payload = {
            'apiKey': self.api_key
        }

    def send_delete_request(self, path: str, request_param: Optional[dict] = None) -> Response:
        data_ = convert_bool_to_str(request_param)
        return requests.delete(url=self.api_url + path, data=data_, params=self.payload)

    def send_get_request(self, path: str, url_param: Optional[dict] = None) -> Response:
        params = self.payload.copy()
        if url_param:
            for key, value in convert_bool_to_str(url_param).items():
                params[key] = value
        _url = self.api_url + path
        return requests.get(url=(self.api_url + path), params=params)

    def send_patch_request(self, path: str, request_param: dict) -> Response:
        data_ = convert_bool_to_str(request_param)
        return requests.patch(url=(self.api_url + path), data=data_, params=self.payload)

    def send_post_request(self, path: str, request_param: dict) -> Response:
        data_ = convert_bool_to_str(request_param)
        return requests.post(url=(self.api_url + path), data=data_, params=self.payload)

    def send_put_request(self, path: str, request_param: dict) -> Response:
        data_ = convert_bool_to_str(request_param)
        return requests.put(url=(self.api_url + path), data=data_, params=self.payload)

    def get_file(self, path: str, url_param) -> Tuple[str, Response]:
        # ↓ホントにこんなダラダラ書く必要あんのかな・・？
        def get_file_name(content_disposition_header: str):
            fn = content_disposition_header[
                 content_disposition_header.find('filename') + len('filename'):len(content_disposition_header)]
            m = fn.find('*=')
            fn2 = fn
            if not m == -1:
                fn2 = fn[:m] + fn[m + 2:]
            m = re.search("UTF-8''", fn2)
            if not m:
                return fn2
            return fn2[:m.start()] + fn2[m.end():]

        params = self.payload.copy()
        if url_param:
            for p in url_param:
                params[p] = url_param[p]
        response = requests.get(url=(self.api_url + path), params=params)
        if not response.ok:
            return '', response
        filename = get_file_name(response.headers['Content-Disposition'])
        with open('tmp/{filename}'.format(filename=filename), mode='wb') as save_file:
            save_file.write(response.content)
        return 'tmp/{filename}'.format(filename=filename), response

    def post_file(self, path: str, files: dict) -> Response:
        return requests.post(url=(self.api_url + path), files=files, params=self.payload)
