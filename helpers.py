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

def rotate(array):
    return array[1:] + array[:1]

def request(servers, directory):
    time.sleep(1)

    max_request_attempts = len(servers) * 2
    request_attempts = 0

    while request_attempts < max_request_attempts:
        # request resource from first server in list
        url = "http://tagpro-%s.koalabeast.com%s" % (servers[0], directory)
        response = requests.get(url)

        if response.ok:
            return response
        else:
            # rotate our copy of server list
            servers = rotate(servers)
            request_attempts += 1
