from datetime import datetime


def get_YYYYMMDDHHMMSS_name(prefix: str, now: datetime) -> str:
    return prefix + '_{YYYYMMDDHHMMSS}'.format(YYYYMMDDHHMMSS=now.strftime('%Y%m%d%H%M%S'))


now = datetime.now()
webhook_endpoint = 'http://webhook.example.com/'  # ダミー URL


basic_issue_data = {
    'summary': get_YYYYMMDDHHMMSS_name('summary', now),
    'priority_id': 1,
    'description': 'test_description',
    'start_date': '2019-01-01',
    'due_date': '2100-12-31',
}

basic_user_data = {
    'user_id': get_YYYYMMDDHHMMSS_name('test_user', now),
    'password': 'password',
    'name': get_YYYYMMDDHHMMSS_name('テストユーザー', now),
    'mail_address': 'test2@example.com',
    'role_type': 2,
}

basic_version_data = {
    'name': get_YYYYMMDDHHMMSS_name('version', now),
    'description': 'test_description',
    'start_date': '2020-07-07',
    'release_due_date': '2020-12-31',
}

basic_watching_data = {
    'note': get_YYYYMMDDHHMMSS_name('test', now)
}

basic_wiki_data = {
    'name': get_YYYYMMDDHHMMSS_name('test_wiki', now=now),
    'content': 'wiki body',
    'mail_notify': False,
}


basic_webhook_data = {
    'name': get_YYYYMMDDHHMMSS_name('webhook', now),
    'description': 'test webhook',
    'hook_url': webhook_endpoint,
    'all_event': False,
    'activity_type_ids': [1, 2, 3, 4, 5]
}

updated_issue_data = {
    'summary': get_YYYYMMDDHHMMSS_name('summary_2', now),
    'priority_id': 3,
    'description': 'test_description_updated',
    'start_date': '2020-01-01',
    'due_date': '2099-12-31',
}

updated_version_data = {
    'name': get_YYYYMMDDHHMMSS_name('version_2', now),
    'description': 'updated_description',
    'start_date': '2020-12-01',
    'release_due_date': '2020-12-31',
    'archived': True,
}

updated_watching_data = {
    'note': get_YYYYMMDDHHMMSS_name('test_2', now)
}

updated_webhook_data = {
    'name': get_YYYYMMDDHHMMSS_name('webhook2', now),
    'description': 'updated webhook',
    'hook_url': webhook_endpoint,
    'all_event': False,
    'activity_type_ids': [5, 6, 7, 8]
}


updated_wiki_data = {
    'name': get_YYYYMMDDHHMMSS_name('Wiki2_', now),
    'content': 'updated wiki body',
    'mail_notify': True,
}
