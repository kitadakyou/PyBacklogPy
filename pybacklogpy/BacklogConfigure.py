class BacklogConfigure:
    def __init__(self, space_id: str, api_key: str, domain: str):
        self.api_url = space_id + domain
        self.api_key = api_key


class BacklogComConfigure(BacklogConfigure):
    def __init__(self, space_id: str, api_key: str):
        super(BacklogComConfigure, self).__init__(space_id, api_key, '.backlog.com')


class BacklogJpConfigure(BacklogConfigure):
    def __init__(self, space_id: str, api_key: str):
        super(BacklogJpConfigure, self).__init__(space_id, api_key, '.backlog.jp')


class BacklogToolConfigure(BacklogConfigure):
    def __init__(self, space_id: str, api_key: str):
        super(BacklogToolConfigure, self).__init__(space_id, api_key, '.backlogtool.com')
