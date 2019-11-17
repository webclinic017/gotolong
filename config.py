import os
import sys

from dateutil.relativedelta import relativedelta
import datetime

from configparser import ConfigParser

class Config(object):
    config_der_hold_max = 1
    config_der_buy_max = 0.50

    config_roce3_buy_min = 12
    config_roce3_hold_min = 6

    config_dpr3_buy_min = 10
    config_dpr3_hold_min = 5

    def __init__(self):
        super(Config, self).__init__()
        parser = ConfigParser()
        parser.read(self.get_config_file())
        self.config_der_hold = parser.get('DEFAULT', 'der_hold')
        self.config_der_buy = parser.get('DEFAULT', 'der_buy')
        self.config_roce3_buy = parser.get('DEFAULT', 'roce3_buy')
        self.config_roce3_hold = parser.get('DEFAULT', 'roce3_hold')
        self.config_dpr3_buy = parser.get('DEFAULT', 'dpr3_buy')
        self.config_dpr3_hold = parser.get('DEFAULT', 'dpr3_hold')
        self.DB_FILENAME = 'equity.sqlite3'
        # started investment in year 2017
        start_date = datetime.date(2017, 1, 1)
        end_date = datetime.date.today()
        self.INVEST_YEARS = relativedelta(end_date, start_date).years
        self.INVEST_YEARS += 1

    # print 'investing for ', self.INVEST_YEARS, ' years'

    def get_root(self):
        # print globals()
        # print '__file__ : ', __file__
        config_root = os.path.abspath(os.path.dirname(__file__))
        config_root = config_root.replace("Google Drive", r"""'Google Drive'""")
        # print(config_root)
        return config_root

    def get_src(self):
        return os.path.join(self.get_root(), 'src')

    def get_data(self):
        return os.path.join(self.get_root(), 'input-global-data')

    def get_reports(self):
        return os.path.join(self.get_root(), 'output-global-reports')

    def get_profile_data(self):
        return os.path.join(self.get_root(), 'input-user-data')

    def get_profile_reports(self):
        return os.path.join(self.get_root(), 'output-user-reports')

    def get_db_files(self):
        return os.path.join(self.get_root(), 'db-files')

    def get_db_schema(self):
        return os.path.join(self.get_root(), 'db-schema')

    def get_config_file(self):
        return os.path.join(self.get_root(), 'config.ini')


if __name__ == "__main__":
    import config

    config = config.Config();

    cmd = sys.argv[1]
    if cmd == "root":
        print(config.get_root())
    elif cmd == "src":
        print(config.get_src())
    elif cmd == "data":
        print(config.get_data())
    elif cmd == "reports":
        print(config.get_reports())
    elif cmd == "profile_data":
        print(config.get_profile_data())
    elif cmd == "profile_reports":
        print(config.get_profile_reports())
    elif cmd == "db_files":
        print(config.get_db_files())
    elif cmd == "db_schema":
        print(config.get_db_schema())
