import loadConfig
# from loadConfig import LoadConfig
import requests


class User:
    def __init__(self):
        self.cfg = loadConfig.LoadConfig()
        self.domain = self.cfg.get_config_data()
        # print(domain)
        self.cookies = self.cfg.get_cookie_data()
        self.f = '/conf.conf'
        self.user_id = ''
        self.username = ''
        self.real_name = ''
        self.available_money = 0
        self.total_in = 0
        self.total_out = 0
        self.total_profit = 0
        self.withdrawable_money = 0
        self.bonus_balance = 0
        self.need_flow = 0
        self.get_user_info()
        self.acc = []
        self.acc.append(self.available_money)
        self.acc.append(self.total_in)
        self.acc.append(self.total_out)
        self.acc.append(self.total_profit)
        self.acc.append(self.withdrawable_money)
        self.acc.append(self.bonus_balance)
        self.acc.append(self.need_flow)

    def get_user_info(self):
        view_path = '/user/view'
        # cfg = loadConfig.LoadConfig()
        # domain = cfg.get_config_data()
        # # print(domain)
        # cookies = cfg.get_cookie_data()
        # print(cookies)
        url = self.domain + view_path
        # file = '/conf.conf'
        section = 'user.view'
        req_data = self.cfg.get_request_data(self.f, section)
        data = eval(req_data['data'])
        res = requests.post(url=url, cookies=self.cookies, data=data).json()
        # print(res)
        self.user_id = res['data']['user']['id']
        self.username = res['data']['user']['username']
        self.real_name = res['data']['user']['real_name']
        self.available_money = float(res['data']['userAccountStats']['available_money'])
        self.total_in = float(res['data']['userAccountStats']['total_in'])
        self.total_out = float(res['data']['userAccountStats']['total_out'])
        self.total_profit = float(res['data']['userAccountStats']['total_profit'])
        self.withdrawable_money = float(res['data']['userAccountStats']['withdrawable_money'])
        self.bonus_balance = float(res['data']['userAccountDeposit']['bonus_balance'])
        self.need_flow = float(res['data']['userAccountDeposit']['need_flow'])
        # print(res.status_code)
        # print(res.text)
        # print(type(res.json()))

    def get_quota_change_list(self):
        # 获取用户额度修正列表
        quota_path = '/ticket/quota-change-list'
        # cfg = loadConfig.LoadConfig()
        # domain = cfg.get_config_data()
        # cookies = cfg.get_cookie_data()
        url = self.domain + quota_path
        section = 'ticket.quota-change-list'
        file = r'\user.conf'
        data = self.cfg.get_request_paras(file, section)
        data['data[user_name]'] = self.username
        res = requests.post(url=url, cookies=self.cookies, data=data).json()
        return res

    def get_quota_ticket_id(self):
        # 返回最近的一条额度修正ticket_id
        res = self.get_quota_change_list()
        ticket_id = res['data']['list'][0]['ticket_id']
        return ticket_id

    def get_quota_ticket_id(self, num):
        # 返回前num条额度修正ticket_id，返回值位list
        res = self.get_quota_change_list()
        if isinstance(num, int):
            ticket_id = []
            for i in range(num):
                ticket_id.append(res['data']['list'][i]['ticket_id'])
            return ticket_id
        else:
            raise AssertionError('para error !')

    def get_deposit_list(self):
        # 获取会员存款列表
        quota_path = '/ticket/deposit-list'
        # cfg = loadConfig.LoadConfig()
        # domain = cfg.get_config_data()
        # cookies = cfg.get_cookie_data()
        url = self.domain + quota_path
        section = 'ticket.deposit-list'
        file = r'\user.conf'
        data = self.cfg.get_request_paras(file, section)
        data['data[user_name]'] = self.username
        res = requests.post(url=url, cookies=self.cookies, data=data).json()
        return res

    def get_deposit_ticket_id(self):
        # 返回最近一条会员存款ticket_id
        res = self.get_deposit_list()
        ticket_id = res['data']['list'][0]['ticket_id']
        return ticket_id

    def get_deposit_ticket_id(self, num):
        # 返回前num条会员存款ticket_id
        res = self.get_deposit_list()
        if isinstance(num, int):
            ticket_id = []
            for i in range(num):
                ticket_id.append(res['data']['list'][i]['ticket_id'])
            return ticket_id
        else:
            raise AssertionError('para error !')

    def get_withdraw_list(self):
        # 获取取款人工审核列表
        quota_path = '/ticket/withdraw-list'
        # cfg = loadConfig.LoadConfig()
        # domain = cfg.get_config_data()
        # cookies = cfg.get_cookie_data()
        url = self.domain + quota_path
        section = 'ticket.withdraw-list'
        file = r'\user.conf'
        data = self.cfg.get_request_paras(file, section)
        data['data[user_name]'] = self.username
        res = requests.post(url=url, cookies=self.cookies, data=data).json()
        return res

    def get_withdraw_ticket_id(self):
        # 返回最近一条会员取款ticket_id
        res = self.get_withdraw_list()
        ticket_id = res['data']['list'][0]['ticket_id']
        return ticket_id

    def get_withdraw_ticket_id(self, num=0):
        # 返回前num条会员存款ticket_id
        res = self.get_withdraw_list()
        if isinstance(num, int):
            ticket_id = []
            for i in range(num):
                ticket_id.append(res['data']['list'][i]['ticket_id'])
            return ticket_id
        else:
            raise AssertionError('para error !')

    def examine_operates(self, ticket_id, operate):
        """ticket_id :
           operate:1 通过   2 拒绝
        """
        examine_path = '/ticket/examine-operates'
        url = self.domain + examine_path
        section = 'ticket.examine-operates'
        file = r'\user.conf'
        data = self.cfg.get_request_paras(file=file, section=section)
        data['operate'] = operate
        data['ticket_id'] = ticket_id
        res = requests.post(url=url, data=data, cookies=self.cookies).json()
        if res['status']['err_code'] != 0:
            raise AssertionError('提案审核失败！')


if __name__ == '__main__':
    user = User()
    # print(user.available_money)
    # print(user.username)
    # print(user.available_money == 9389.0)
    # print(type(user.available_money))
    # print(user.get_quota_ticket_id())
    # print(user.get_deposit_ticket_id())
    print(user.get_withdraw_ticket_id())
