import unittest
import requests
from common import loadConfig
from common import user
import sys

sys.path.append('../common')


class QuotaChangeDes(unittest.TestCase):
    def setUp(self):
        self.user_name = ''
        self.real_name = ''
        self.cfg = loadConfig.LoadConfig()
        self.url = self.cfg.get_config_data() + '/send-ticket/quota-change'
        self.file = '\quota-change.conf'
        self.quota_change = 100
        self.cookies = self.cfg.get_cookie_data()

    def compare_acc(self, before, after):
        if len(before) != len(after):
            raise AssertionError('list length not equal !')
        res = []
        for i in range(len(before)):
            res.append(after[i] - before[i])
        return res

    def base_correct_type(self, currency, corrected_type, operation, flow_multi=0, quota_change=100):
        """currency :1 现金 2 彩金
           corrected_type:额度转移类型
           operation：0减少，1增加
           flow_multi：流水倍数
           quota_change:额度变化值
        """
        section = 'send-ticket.quota-change'
        data = self.cfg.get_request_paras(file=self.file, section=section)
        data['currency'] = currency
        data['corrected_type'] = corrected_type
        data['operation'] = operation
        data['flow_multi'] = flow_multi
        data['quota_change'] = quota_change
        data['user_name'] = self.user_name
        data['real_name'] = self.real_name
        cookies = self.cookies
        res = requests.post(url=self.url, cookies=cookies, data=data).json()
        return res

    def base_correct_type(self, currency, corrected_type, operation, flow_multi=0):
        """currency :1 现金 2 彩金
           corrected_type:额度转移类型
           operation：0减少，1增加
           flow_multi：流水倍数
        """
        section = 'send-ticket.quota-change'
        data = self.cfg.get_request_paras(file=self.file, section=section)
        data['currency'] = currency
        data['corrected_type'] = corrected_type
        data['operation'] = operation
        data['flow_multi'] = flow_multi
        data['quota_change'] = self.quota_change
        data['user_name'] = self.user_name
        data['real_name'] = self.real_name
        cookies = self.cookies
        res = requests.post(url=self.url, cookies=cookies, data=data).json()
        return res

    def test_corrected_type_des_money_9(self):
        """额度转移减现金"""
        before = user.User()
        print(before.acc)
        self.user_name = before.username
        self.real_name = before.real_name
        currency = 1
        corrected_type = 9
        operation = 0
        res = self.base_correct_type(currency, corrected_type, operation)
        print(res)
        self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
        after = user.User()
        print(after.acc)
        actual = self.compare_acc(before.acc, after.acc)
        print(actual)
        expect = [-float(self.quota_change), 0.0, 0.0, 0.0, -float(self.quota_change), 0.0, 0.0]
        self.assertEqual(actual, expect, msg='account error !')

    def test_corrected_type_des_bon_9(self):
        """额度转移减彩金"""
        before = user.User()
        print(before.acc)
        self.user_name = before.username
        self.real_name = before.real_name
        currency = 2
        corrected_type = 9
        operation = 0
        res = self.base_correct_type(currency, corrected_type, operation)
        print(res)
        self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
        after = user.User()
        print(after.acc)
        actual = self.compare_acc(before.acc, after.acc)
        print(actual)
        expect = [0.0, 0.0, 0.0, 0.0, 0.0, -float(self.quota_change), 0.0]
        self.assertEqual(actual, expect, msg='account error !')


if __name__ == '__main__':
    unittest.main(verbosity=2)
