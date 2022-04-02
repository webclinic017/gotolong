#!/usr/bin/env python

import os
import re

# 10k
heroku_db_row_limits = 10000

def main():
    debug = 0
    total_db_rows_count = 0
    data = os.environ.get('GOTOLONG_DATA')
    print(data)

    db_stats_file = data + "/db/" + 'gotolong_db_stats.txt'
    print(db_stats_file)

    with open(db_stats_file) as reader:
        for line in reader:
            if debug:
                print(line)
            m = re.match(r"\|\s*(\w+)\s*\|\s*(\d+)\s*\|", line)
            if m != None and int(m.group(2)) != 0:
                table_name = m.group(1)
                table_rows = m.group(2)
                total_db_rows_count += int(table_rows)
                print('total_db_rows_count : ' + str(
                    total_db_rows_count) + ' added table ' + table_name + ' rows ' + table_rows)
    print('db: total rows of all tables ' + str(total_db_rows_count))
    if total_db_rows_count > heroku_db_row_limits:
        print('ERROR: Exceeded heroku db row limits of ' + str(heroku_db_row_limits))


if __name__ == "__main__":
    main()
