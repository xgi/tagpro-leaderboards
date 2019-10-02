import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

name_associations = {
    'day': 'Daily',
    'week': 'Weekly',
    'month': 'Monthly'
}


def submission_title(date, board_name):
    if board_name == "day":
        date_string = date.strftime('%A, %B %d, %Y')
    elif board_name == "week":
        date_string = date.strftime('%B %d, %Y')
    elif board_name == "month":
        # monthly boards are reset during the 1st, so we need the name of the
        # previous month
        prev_time = date - relativedelta(months=1)
        date_string = prev_time.strftime('%B %Y')
    else:
        raise ValueError("Invalid board name argument; valid names are "
                         "day/week/month")

    submission_title = "%s Leaderboard Log/Statistics for %s" %\
        (name_associations[board_name], date_string)

    return submission_title


def time_str(seconds):
    # https://stackoverflow.com/a/8907407
    hours, remainder = divmod(int(seconds), 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)
