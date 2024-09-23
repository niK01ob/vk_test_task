from lib import constants as c
from lib import stat

import datetime
import os
import sys

if __name__ == '__main__':

    date = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
    users_stat = {}
    for i in range(c.WEEK_DAYS_COUNT):
        date_of_stat = date - datetime.timedelta(days=i+1)
        stat_for_day = stat.get_stat_for_day(date_of_stat.strftime('%Y-%m-%d'))
        for email, count_for_action in stat_for_day.items():
            if email not in users_stat:
                users_stat[email] = {}
            for action, count in count_for_action.items():
                if action not in users_stat[email]:
                    users_stat[email][action] = 0
                users_stat[email][action] += count

    print(users_stat)
    stat.write_stat(date.strftime('%Y-%m-%d'), c.OUT_DIR_NAME, users_stat)
