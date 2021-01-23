import os
import sys

from dateutil.relativedelta import relativedelta
import datetime

from configparser import ConfigParser


class GotoLong_Config(object):

    def __init__(self):
        super(GotoLong_Config, self).__init__()
        self.cp = ConfigParser(os.environ)
        self.cp.read(self.get_config_file())
        self.config_db_type = self.cp.get('DATABASE', 'db_type')
        self.config_db_name = self.cp.get('DATABASE', 'db_name')
        self.config_db_user = self.cp.get('DATABASE', 'db_user')
        self.config_db_pass = self.cp.get('DATABASE', 'db_pass')

        self.config_loc_global_data = self.cp.get('LOCATION', 'GLOBAL_DATA')
        self.config_loc_global_reports = self.cp.get('LOCATION', 'GLOBAL_REPORTS')
        self.config_loc_profile_data = self.cp.get('LOCATION', 'PROFILE_DATA')
        self.config_loc_profile_reports = self.cp.get('LOCATION', 'PROFILE_REPORTS')
        self.config_loc_db_schema = self.cp.get('LOCATION', 'DB_SCHEMA_LOC')

        self.config_der_hold = float(self.cp.get('FILTER', 'der_hold'))
        self.config_der_buy = float(self.cp.get('FILTER', 'der_buy'))
        self.config_icr_hold = float(self.cp.get('FILTER', 'icr_hold'))
        self.config_icr_buy = float(self.cp.get('FILTER', 'icr_buy'))
        self.config_roce3_buy = float(self.cp.get('FILTER', 'roce3_buy'))
        self.config_roce3_hold = float(self.cp.get('FILTER', 'roce3_hold'))
        self.config_dpr3_buy = float(self.cp.get('FILTER', 'dpr3_buy'))
        self.config_dpr3_hold = float(self.cp.get('FILTER', 'dpr3_hold'))
        self.config_dpr2_buy = float(self.cp.get('FILTER', 'dpr2_buy'))
        self.config_dpr2_hold = float(self.cp.get('FILTER', 'dpr2_hold'))

        self.config_sales5_buy = float(self.cp.get('FILTER', 'sales5_buy'))
        self.config_sales5_hold = float(self.cp.get('FILTER', 'sales5_hold'))

        self.config_sales2_buy = float(self.cp.get('FILTER', 'sales2_buy'))
        self.config_sales2_hold = float(self.cp.get('FILTER', 'sales2_hold'))

        self.config_profit5_buy = float(self.cp.get('FILTER', 'profit5_buy'))
        self.config_profit5_hold = float(self.cp.get('FILTER', 'profit5_hold'))

        self.config_pledge_buy = float(self.cp.get('FILTER', 'pledge_buy'))
        self.config_pledge_hold = float(self.cp.get('FILTER', 'pledge_hold'))
        self.config_rank_buy = float(self.cp.get('FILTER', 'rank_buy'))
        self.config_rank_hold = float(self.cp.get('FILTER', 'rank_hold'))
        self.config_lc_weight = float(self.cp.get('FILTER', 'lc_weight'))
        self.config_mc_weight = float(self.cp.get('FILTER', 'mc_weight'))
        self.config_sc_weight = float(self.cp.get('FILTER', 'sc_weight'))
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
        # config_root = os.path.abspath(os.path.dirname(__file__))
        # config_root = config_root.replace("Google Drive", r"""'Google Drive'""")
        config_root = os.environ.get('GOTOLONG_DATA')
        # remove /src
        # print(config_root)
        return config_root

    def get_data(self):
        return self.get_root()

    def get_global_data(self):
        return os.path.join(self.get_data(), self.config_loc_global_data)

    def get_global_reports(self):
        return os.path.join(self.get_data(), self.config_loc_global_reports)

    def get_profile_data(self):
        return os.path.join(self.get_data(), self.config_loc_profile_data)

    def get_profile_reports(self):
        return os.path.join(self.get_data(), self.config_loc_profile_reports)

    def get_db_name(self):
        return self.config_db_name

    def get_db_user(self):
        return self.config_db_user

    def get_db_pass(self):
        return self.config_db_pass

    def get_db_schema(self):
        return os.path.join(self.get_data(), self.config_loc_db_schema)

    def get_config_file(self):
        return os.path.join(self.get_data(), 'config/gotolong-config.ini')


def main():
    config = GotoLong_Config()

    if (len(sys.argv)) < 2:
        print('usage: ' + sys.argv[0] + ' <command>')
        print('usage: ' + sys.argv[0] + ' root | src | data')
        print('usage: ' + sys.argv[0] + ' global_data | global_reports')
        print('usage: ' + sys.argv[0] + ' profile_data | profile_reports')
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "root":
        print(config.get_root())
    elif cmd == "data":
        print(config.get_data())
    elif cmd == "global_data":
        print(config.get_global_data())
    elif cmd == "global_reports":
        print(config.get_global_reports())
    elif cmd == "profile_data":
        print(config.get_profile_data())
    elif cmd == "profile_reports":
        print(config.get_profile_reports())
    elif cmd == "db_name":
        print(config.get_db_name())
    elif cmd == "db_user":
        print(config.get_db_user())
    elif cmd == "db_pass":
        print(config.get_db_pass())
    elif cmd == "db_schema":
        print(config.get_db_schema())


if __name__ == "__main__":
    main()
