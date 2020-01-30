#!/usr/bin/python

import re


def normalize_comp_name(comp_name):
    # Capitalize
    comp_name = comp_name.capitalize()

    # remove hyphen (V-guard)
    comp_name = re.sub('-', ' ', comp_name)

    # remove . in Dr. lal pathlabs
    comp_name = re.sub('\.', '', comp_name)

    # remove ' in Dr Reddy's Laboratories
    comp_name = re.sub('\'', '', comp_name)

    # removed limited and india
    comp_name = re.sub('limited', '', comp_name)
    comp_name = re.sub('ltd', '', comp_name)
    comp_name = re.sub('india', '', comp_name)
    comp_name = re.sub(' of ', '', comp_name)

    # replace and and &
    comp_name = re.sub(' and ', ' ', comp_name)
    comp_name = re.sub(' & ', ' ', comp_name)

    # replace , (amfi data)
    comp_name = re.sub(',', '', comp_name)

    # replace inds (for screener)
    comp_name = re.sub('inds', '', comp_name)

    # remove any characters after (  :
    # TRENT LTD (LAKME LTD)
    comp_name = re.sub('\(.*', '', comp_name)

    # convert multiple space to single space
    comp_name = re.sub(' +', ' ', comp_name)

    # combine H D F C into HDFC
    comp_name_list = list(comp_name)
    even_char = comp_name_list[0::2]
    odd_char = comp_name_list[1::2]
    if len(set(odd_char)) == 1:
        if odd_char[0] == ' ':
            new_comp_name = ''.join(even_char)
            print('converted : ', comp_name, ' to ', new_comp_name)
            comp_name = new_comp_name

    # remove corpn in screener
    comp_name = re.sub('corpn', '', comp_name)

    # strip space
    comp_name = comp_name.strip()

    return comp_name


def get_number(num_str):
    # strip space
    num_str = str(num_str).strip()
    if num_str == 'NaN':
        num_str = '0'

    # remove comma
    num_str = num_str.replace(',', '')

    if num_str == '':
        num_str = '0'

    return int(round(float(num_str)))


def get_insert_sql(table_name, table_dict):
    insert_sql = "insert into "
    insert_sql += table_name
    insert_sql += "("

    iter = 0
    for column_name in table_dict:
        insert_sql += column_name
        if iter != len(table_dict) - 1:
            insert_sql += ","
        iter += 1

    insert_sql += ") values("

    iter = 0
    for column_name in table_dict:

        insert_sql += "%s"
        # insert_sql += ":"
        # insert_sql += table_dict[column_name]

        if iter != len(table_dict) - 1:
            insert_sql += ","

        iter += 1
    insert_sql += ")"

    print(insert_sql)

    return insert_sql


def get_create_sql(table_name, table_dict):
    create_sql = "create table if not exists "
    create_sql += table_name
    create_sql += "("

    iter = 0
    for column_name in table_dict:
        create_sql += column_name
        create_sql += " " + table_dict[column_name]
        if iter != len(table_dict) - 1:
            create_sql += ","
        iter += 1
    create_sql += ")"
    print(create_sql)

    return create_sql
