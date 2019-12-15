from requests import Response
from typing import List, Optional

from pybacklogpy.BacklogConfigure import BacklogConfigure
from pybacklogpy.modules import RequestSender


class Status:
    def __init__(self, config: Optional[BacklogConfigure] = None):
        self.base_path = 'statuses'
        _config = config if config else None
        self.rs = RequestSender(_config)
