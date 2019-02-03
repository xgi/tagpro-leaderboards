import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

name_associations = {
    'day': 'Daily',
    'week': 'Weekly',
    'month': 'Monthly'
}


def submission_title(board_name):
    cur_time = datetime.utcnow()

    if board_name == "day":
        date_string = cur_time.strftime('%B %d, %Y')
    elif board_name == "week":
        date_string = cur_time.strftime('%B %d, %Y')
    elif board_name == "month":
        # monthly boards are reset during the 1st, so we need the name of the
        # previous month
        prev_time = cur_time - relativedelta(months=1)
        date_string = prev_time.strftime('%B %Y')
    else:
        raise ValueError("Invalid board name argument; valid names are "
                         "day/week/month")

    submission_title = "%s Leaderboard Log/Statistics for %s" %\
        (name_associations[board_name], date_string)

    return submission_title


def time_str(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(int(seconds)))
