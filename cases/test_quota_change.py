import unittest
import requests
import copy
import sys

sys.path.append('../common')
from common import loadConfig
from common import user


def compare_acc(before, after):
    print('===============account_compare============')
    if len(before) != len(after):
        raise AssertionError('list length not equal !')
    res = []
    for i in range(len(before)):
        res.append(after[i] - before[i])
    print(res)
    return res


class QuotaChangeDes(unittest.TestCase):
    def setUp(self):
        self.user = user.User()
        self.user_name = self.user.username
        self.real_name = self.user.real_name
        self.cfg = loadConfig.LoadConfig()
        self.url = self.cfg.get_config_data() + '/send-ticket/quota-change'
        self.file = '\quota-change.conf'
        self.quota_change = 100
        self.cookies = self.cfg.get_cookie_data()

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

    def test_corrected_type_des_9_money(self):
        """额度转移减现金"""
        before = copy.copy(self.user.get_user_acc())
        print('before account is :{0}'.format(before))
        currency = 1
        corrected_type = 9
        operation = 0
        res = self.base_correct_type(currency, corrected_type, operation)
        print(res)
        self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
        self.user.get_user_info()
        after = copy.copy(self.user.get_user_acc())
        print('after account is :{0}'.format(after))
        actual = compare_acc(before, after)
        expect = [-float(self.quota_change), 0.0, 0.0, 0.0, -float(self.quota_change), 0.0, 0.0]
        self.assertEqual(actual, expect, msg='account error !')

    def test_corrected_type_des_9_money_rej(self):
        """拒绝额度转移减现金"""
        before = copy.copy(self.user.get_user_acc())
        print('before account is :{0}'.format(before))
        currency = 1
        corrected_type = 9
        operation = 0
        res = self.base_correct_type(currency, corrected_type, operation)
        print(res)
        self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
        self.user.get_user_info()
        after = copy.copy(self.user.get_user_acc())
        print('after account is :{0}'.format(after))
        actual = compare_acc(before, after)
        expect = [-float(self.quota_change), 0.0, 0.0, 0.0, -float(self.quota_change), 0.0, 0.0]
        self.assertEqual(actual, expect, msg='account error !')

        self.user.examine_operates(self.user.get_quota_ticket_id(num=1), 2)  # 审核拒绝

        self.user.get_user_info()
        final = copy.copy(self.user.acc)  # 审核拘谨后
        print('final account is :{0}'.format(final))
        actual_2 = compare_acc(before, final)
        expect_2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(actual_2, expect_2, msg='account error !')

    def test_corrected_type_des_9_bon(self):
        """额度转移减彩金"""
        before = copy.copy(self.user.acc)
        print('before account is :{0}'.format(before))
        currency = 2
        corrected_type = 9
        operation = 0
        res = self.base_correct_type(currency, corrected_type, operation)
        print(res)
        self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
        self.user.get_user_info()
        after = copy.copy(self.user.acc)
        print('after account is :{0}'.format(after))
        actual = compare_acc(before, after)
        expect = [0.0, 0.0, 0.0, 0.0, 0.0, -float(self.quota_change), 0.0]
        self.assertEqual(actual, expect, msg='account error !')

    def test_corrected_type_add_9_money(self):
        """额度转移加现金0/1/2倍流水"""
        for i in range(3):
            print('=====额度转移加现金{0}倍流水======'.format(i))
            before = copy.copy(self.user.acc)  # 额度修正前
            print('before account is :{0}'.format(before))
            currency = 1
            corrected_type = 9
            operation = 1
            flow_multi = i
            print('flow_multi is {0}'.format(flow_multi))
            res = self.base_correct_type(currency, corrected_type, operation, flow_multi=flow_multi)
            print(res)
            self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
            self.user.get_user_info()
            after = copy.copy(self.user.acc)  # 额度修正后
            print('after account is :{0}'.format(after))
            actual_1 = compare_acc(before, after)
            expect_1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            self.assertEqual(actual_1, expect_1, msg='account error !')

            self.user.examine_operates(self.user.get_quota_ticket_id(num=1), 1)  # 审核通过

            self.user.get_user_info()
            final = copy.copy(self.user.acc)  # 审核通过后
            print('final account is :{0}'.format(final))
            actual_2 = compare_acc(before, final)
            expect_2 = [self.quota_change, 0.0, 0.0, 0.0,
                        self.quota_change, 0.0, self.quota_change * flow_multi]
            self.assertEqual(actual_2, expect_2, msg='account error !')

    def test_corrected_type_add_9_bon(self):
        """额度转移加彩金0/1/2倍流水"""
        for i in range(3):
            print('=====额度转移加现金{0}倍流水======'.format(i))
            before = copy.copy(self.user.acc)  # 额度修正前
            print('before account is :{0}'.format(before))
            currency = 2
            corrected_type = 9
            operation = 1
            flow_multi = i
            print('flow_multi is {0}'.format(flow_multi))
            res = self.base_correct_type(currency, corrected_type, operation, flow_multi=flow_multi)
            print(res)
            self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
            self.user.get_user_info()
            after = copy.copy(self.user.acc)  # 额度修正后
            print('after account is :{0}'.format(after))
            actual_1 = compare_acc(before, after)
            expect_1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            self.assertEqual(actual_1, expect_1, msg='account error !')

            self.user.examine_operates(self.user.get_quota_ticket_id(num=1), 1)  # 审核通过

            self.user.get_user_info()
            final = copy.copy(self.user.acc)  # 审核通过后
            print('final account is :{0}'.format(final))
            actual_2 = compare_acc(before, final)
            expect_2 = [0.0, 0.0, 0.0, 0.0,
                        0.0, self.quota_change, self.quota_change * flow_multi]
            self.assertEqual(actual_2, expect_2, msg='account error !')

    def test_corrected_type_des_8_money(self):
        """测试账号减现金"""
        before = copy.copy(self.user.acc)
        print('before account is :{0}'.format(before))
        currency = 1
        corrected_type = 8
        operation = 0
        res = self.base_correct_type(currency, corrected_type, operation)
        print(res)
        self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
        self.user.get_user_info()
        after = copy.copy(self.user.acc)
        print('after account is :{0}'.format(after))
        actual = compare_acc(before, after)
        expect = [-float(self.quota_change), 0.0, 0.0, 0.0, -float(self.quota_change), 0.0, 0.0]
        self.assertEqual(actual, expect, msg='account error !')

    def test_corrected_type_add_8_money(self):
        """测试账号加现金0/1/2倍流水"""
        for i in range(3):
            print('=====额度转移加现金{0}倍流水======'.format(i))
            before = copy.copy(self.user.acc)  # 额度修正前
            print('before account is :{0}'.format(before))
            currency = 1
            corrected_type = 8
            operation = 1
            flow_multi = i
            print('flow_multi is {0}'.format(flow_multi))
            res = self.base_correct_type(currency, corrected_type, operation, flow_multi=flow_multi)
            print(res)
            self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
            self.user.get_user_info()
            after = copy.copy(self.user.acc)  # 额度修正后
            print('after account is :{0}'.format(after))
            actual_1 = compare_acc(before, after)
            expect_1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            self.assertEqual(actual_1, expect_1, msg='account error !')

            self.user.examine_operates(self.user.get_quota_ticket_id(num=1), 1)  # 审核通过

            self.user.get_user_info()
            final = copy.copy(self.user.acc)  # 审核通过后
            print('final account is :{0}'.format(final))
            actual_2 = compare_acc(before, final)
            expect_2 = [self.quota_change, 0.0, 0.0, 0.0,
                        self.quota_change, 0.0, self.quota_change * flow_multi]
            self.assertEqual(actual_2, expect_2, msg='account error !')

    def test_corrected_type_add_8_bon(self):
        """测试账号加彩金0/1/2倍流水"""
        for i in range(3):
            print('=====额度转移加现金{0}倍流水======'.format(i))
            before = copy.copy(self.user.acc)  # 额度修正前
            print('before account is :{0}'.format(before))
            currency = 2
            corrected_type = 8
            operation = 1
            flow_multi = i
            print('flow_multi is {0}'.format(flow_multi))
            res = self.base_correct_type(currency, corrected_type, operation, flow_multi=flow_multi)
            print(res)
            self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
            self.user.get_user_info()
            after = copy.copy(self.user.acc)  # 额度修正后
            print('after account is :{0}'.format(after))
            actual_1 = compare_acc(before, after)
            expect_1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            self.assertEqual(actual_1, expect_1, msg='account error !')

            self.user.examine_operates(self.user.get_quota_ticket_id(num=1), 1)  # 审核通过

            self.user.get_user_info()
            final = copy.copy(self.user.acc)  # 审核通过后
            print('final account is :{0}'.format(final))
            actual_2 = compare_acc(before, final)
            expect_2 = [0.0, 0.0, 0.0, 0.0,
                        0.0, self.quota_change, self.quota_change * flow_multi]
            self.assertEqual(actual_2, expect_2, msg='account error !')

    def test_corrected_type_des_8_des_rej(self):
        """拒绝测试账号减彩金"""
        before = copy.copy(self.user.get_user_acc())
        print('before account is :{0}'.format(before))
        currency = 2
        corrected_type = 9
        operation = 0
        res = self.base_correct_type(currency, corrected_type, operation)
        print(res)
        self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
        self.user.get_user_info()
        after = copy.copy(self.user.get_user_acc())
        print('after account is :{0}'.format(after))
        actual = compare_acc(before, after)
        expect = [0.0, 0.0, 0.0, 0.0, 0.0, -float(self.quota_change), 0.0]
        self.assertEqual(actual, expect, msg='account error !')

        self.user.examine_operates(self.user.get_quota_ticket_id(num=1), 2)  # 审核拒绝

        self.user.get_user_info()
        final = copy.copy(self.user.acc)  # 审核拘谨后
        print('final account is :{0}'.format(final))
        actual_2 = compare_acc(before, final)
        expect_2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(actual_2, expect_2, msg='account error !')

    def test_corrected_type_des_8_bon(self):
        """测试账号减彩金"""
        before = copy.copy(self.user.acc)
        print('before account is :{0}'.format(before))
        currency = 2
        corrected_type = 8
        operation = 0
        res = self.base_correct_type(currency, corrected_type, operation)
        print(res)
        self.assertEqual(res['status']['err_code'], 0, msg='quota-change request error')
        self.user.get_user_info()
        after = copy.copy(self.user.acc)
        print('after account is :{0}'.format(after))
        actual = compare_acc(before, after)
        expect = [0.0, 0.0, 0.0, 0.0, 0.0, -float(self.quota_change), 0.0]
        self.assertEqual(actual, expect, msg='account error !')


if __name__ == '__main__':
    unittest.main(verbosity=2)