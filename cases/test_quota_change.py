import unittest
import requests
import sys

sys.path.append('../common')
from common import loadConfig
from common import user


class QuotaChangeDes(unittest.TestCase):
    def setUp(self):
        cfg = loadConfig.LoadConfig()
        self.url = cfg.get_config_data() + '/send-ticket/quota-change'
        self.file = '\quota-change.conf'

    def test_corrected_type_9(self):
        before = user.User()
        cfg = loadConfig.LoadConfig()
        section = 'send-ticket.quota-change'
        data = cfg.get_request_paras(file=self.file, section=section)
        data['user_name'] = before.username
        data['real_name'] = before.real_name
        cookies = cfg.get_cookie_data()
        res = requests.post(url=self.url, cookies=cookies, data=data).json()
        self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
        after = user.User()
        self.assertEqual(before.available_money, after.available_money + float(data['quota_change']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
