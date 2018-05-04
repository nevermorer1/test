import configparser
import os
import warnings
import requests

warnings.filterwarnings("ignore")


# import json

class LoadConfig:
    def __init__(self):
        self.f = '\conf.conf'

    def get_config_data(self):
        # 获取后台域名
        # file = '\conf.conf'
        file_path = os.path.abspath('..\config') + self.f
        config = configparser.ConfigParser()
        try:
            config.read(file_path, encoding='utf-8')
            # print(config.sections())
        except Exception as e:
            raise AssertionError("read file err !" + str(e))
            # print(e)
            # return "read file err !"
        # print(config.sections())
        # print(config.items('domain'))
        return config['domain']['domain']

    def get_cookie_data(self):
        # 后台用户登录，获取后续请求header，cookie
        # file = '\conf.conf'
        sec = 'login'
        domain = self.get_config_data()
        url = domain + '/admin/login'
        request_data = self.get_request_data(self.f, sec)
        res = requests.post(url=url, data=eval(request_data['data']))
        # print(res.cookies)
        return res.cookies

    def get_request_data(self, file, section):
        # 获取配置接口参数及请求格式
        # 返回字典res
        file_path = os.path.abspath('..\config') + file
        config = configparser.ConfigParser()
        try:
            config.read(file_path, encoding='utf-8')
            # print(config.sections())
        except Exception as e:
            raise AssertionError("read file err !" + str(e))
            # print(e)
            # return "read file err !"
        if config.has_section(section):
            method = config[section]['method']
            data = config[section]['data']
            # data = eval(config[section]['data'])  ##转换为字典
            res = {'method': method, 'data': data}
            return res
        else:
            raise AssertionError('section not exist !')
            # return 'section not exist !'

    def get_request_paras(self, file, section):
        # 获取配置接口参数
        # 返回字典res
        file_path = os.path.abspath('..\config') + file
        config = configparser.ConfigParser()
        try:
            config.read(file_path, encoding='utf-8')
            # print(config.sections())
        except Exception as e:
            # print(e)
            # return "read file err !"
            raise AssertionError("read file err !" + str(e))
        res = {}
        if config.has_section(section):
            for option in config.options(section):
                res[option] = config.get(section, option)
            return res
        else:
            raise AssertionError('section not exist !')


if __name__ == '__main__':
    #     print(os.path.abspath('..'))
    #     f = '\conf.conf'
    #     cfg = LoadConfig()
    #     cfg.get_cookie_data()
    #     print(cfg.get_config_data(f))
    #         print(f)
    #         s = 'login'
    #     cfg = LoadConfig()
    #     cfg.get_cookie_data()
    #     res = cfg.get_request_data(f, s)
    #     print(res)
    #     print(type(res))
    #     print(type(res['data']))
    f = r'\user.conf'
    s = ['ticket.quota-change-list', 'ticket.deposit-list', 'ticket.withdraw-list']
    cfg = LoadConfig()
    for i in range(len(s)):
        # print(type(cfg.get_request_paras(f, s1)))
        print(cfg.get_request_paras(f, s[i]))
