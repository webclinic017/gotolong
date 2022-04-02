#!/usr/bin/env python

import json
import os
import sys

import gotolong.config.config_ini


def main():
    debug = 0
    config_data = {}

    config = gotolong.config.config_ini.GotoLong_Config()

    config_data['GLOBAL_DATA'] = config.config_loc_global_data
    config_data['GLOBAL_REPORTS'] = config.config_loc_global_reports
    config_data['PROFILE_DATA'] = config.config_loc_profile_data
    config_data['PROFILE_REPORTS'] = config.config_loc_profile_reports

    if debug > 0:
        print(config_data)
        print(config_data['GLOBAL_DATA'])
        print(config_data['GLOBAL_REPORTS'])
        print(config_data['PROFILE_DATA'])
        print(config_data['PROFILE_REPORTS'])

    if len(sys.argv) < 2:
        print('usage:', sys.argv[0], ' module ')
        print('usage:', sys.argv[0], ' amfi')
        exit(1)

    gl_home = os.environ.get('GOTOLONG_DATA')

    module = sys.argv[1]
    json_path = os.path.join(gl_home, 'config/' + module + '.json')

    print(json_path)

    with open(json_path, "r") as read_file:
        data = json.load(read_file)

    cmd_line = ''

    if data['truncate-table'] == 'Yes':
        cmd_line += '-t'
        cmd_line += ' '

    # include logging log
    if 'logging-level' in data:
        cmd_line += '-l ' + data['logging-level']
        cmd_line += ' '

    if 'debug-level' in data:
        cmd_line += '-d ' + data['debug-level']
        cmd_line += ' '

    if 'input-files' in data:
        cmd_line += '-i'
        cmd_line += ' '
        for in_file in data['input-files']:
            if debug > 0:
                print(in_file)
            for k, v in in_file.items():
                if debug > 0:
                    print(k, v)
                if k == 'dir-cfg-key':
                    dir = config_data[v]
                    if debug > 0:
                        print(dir)
                else:
                    file_path = os.path.join(gl_home, dir + '/' + v)
                    cmd_line += file_path
                    cmd_line += ' '

    if 'output-files' in data:
        cmd_line += '-o'
        cmd_line += ' '
        for out_file in data['output-files']:
            if debug > 0:
                print(out_file)
            for k, v in out_file.items():
                if debug > 0:
                    print(k, v)
                if k == 'dir-cfg-key':
                    dir = config_data[v]
                    if debug > 0:
                        print(dir)
                else:
                    file_path = os.path.join(gl_home, dir + '/' + v)
                    if debug > 0:
                        print(file_path, end=' ')
                    cmd_line += file_path
                    cmd_line += ' '

    if debug > 0:
        print(cmd_line)
    return cmd_line


if __name__ == '__main__':
    main()
