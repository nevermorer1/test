import configparser
# test
cfg = configparser.ConfigParser()
#f = 'E:\git\autotest_backend\config\config.ini'
#f = 'config.ini'
f = 'conf.conf'
cfg.read(f)
print(cfg.sections())
print(cfg.has_section('login'))
print(cfg['domain']['domain'])
