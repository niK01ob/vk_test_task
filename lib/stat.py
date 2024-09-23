from . import constants as c


import os
import datetime
import csv


def calc_stat_for_day(date):
    stat = {}
    if f'{date}.csv' not in os.listdir(c.IN_DIR_NAME):
        return stat

    file_path = os.path.join(c.IN_DIR_NAME, f'{date}.csv')
    with open(file_path, 'r', newline='') as input:
        reader = csv.reader(input)
        for row in reader:
            email, action = row[0], row[1].lower()
            if email not in stat:
                stat[email] = {}
            if action not in stat[email]:
                stat[email][action] = 0
            stat[email][action] += 1

    return stat


def write_stat(date, dir_name, stat):
    rows = []
    for email, count_for_action in stat.items():
        row = {'email': email}
        for action in c.ACTIONS:
            row[f'{action}_count'] = 0 if action not in count_for_action else count_for_action[action]
        rows.append(row)

    file_path = os.path.join(dir_name, f'{date}.csv')
    with open(file_path, 'w', newline='') as out:
        if not rows:
            return
        writer = csv.DictWriter(out, rows[0].keys())
        writer.writeheader();
        writer.writerows(rows)


def get_stat_for_day(date):
    stat = {}
    if f'{date}.csv'  not in os.listdir(c.DAILY_DIR_NAME):
        stat = calc_stat_for_day(date)
        write_stat(date, c.DAILY_DIR_NAME, stat)
        return stat

    file_path = os.path.join(c.DAILY_DIR_NAME, f'{date}.csv')
    with open(file_path, 'r', newline='') as input:
        reader = csv.DictReader(input)
        for row in reader:
            stat[row['email']] = {}
            for action in c.ACTIONS: 
                stat[row['email']][action] = int(row[f'{action}_count'])

    return stat
