import json
import os

debug = 0

gl_home = os.environ.get('GOTOLONG_DATA')

if debug > 0:
    print(gl_home)

module = 'config'
json_path = os.path.join(gl_home, 'config/' + module + '.json')
if debug > 0:
    print(json_path)

with open(json_path, "r") as read_file:
    config_data = json.load(read_file)

if debug > 0:
    print(config_data)
    print(config_data['GLOBAL_DATA'])
    print(config_data['GLOBAL_REPORTS'])
    print(config_data['PROFILE_DATA'])
    print(config_data['PROFILE_REPORTS'])

module = 'amfi'
json_path = os.path.join(gl_home, 'config/' + module + '.json')
if debug > 0:
    print(json_path)

with open(json_path, "r") as read_file:
    data = json.load(read_file)

if data['truncate-table'] == 'Yes':
    print('-t', end=' ')

# include logging log
print('-l', data['logging-level'], end=' ')

print('-i', end=' ')
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
            print(file_path, end=' ')

print('-o', end=' ')
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
            print(file_path, end=' ')
