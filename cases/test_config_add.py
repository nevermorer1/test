import unittest
import requests
import sys

sys.path.append('../common')
from common import loadConfig


class CoupleConfig(unittest.TestCase):
    def setUp(self):
        # self.user = user.User()
        # self.user_name = self.user.username
        # self.real_name = self.user.real_name
        self.cfg = loadConfig.LoadConfig()
        self.config_add_url = self.cfg.get_config_data() + '/coupon/config-add'
        print(self.config_add_url)
        self.file = '\conf-add.conf'
        self.cookies = self.cfg.get_cookie_data()

    def test_config_add(self):
        """手动添加彩金"""
        section = 'coupon.config-add'
        data = self.cfg.get_request_paras(file=self.file, section=section)
        print(data)
        for i in range(5):

            res = requests.post(url=self.config_add_url, data=data, cookies=self.cookies,
                                auth=self.cfg.auth).json()
            print(res)
            self.assertEqual(res['status']['err_code'], 0, msg='request error !')
