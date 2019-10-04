#!/bin/python

import praw
from bs4 import BeautifulSoup
import requests
import sys
import os
import random
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime
from dateutil.relativedelta import relativedelta

# local modules
import secret
import helpers
from profile import Profile

# base tagpro server url
BASE_URL = "http://tagpro-test.koalabeast.com"

# validate board name argument
if len(sys.argv) > 1:
    if sys.argv[1] in helpers.name_associations.keys():
        board_name = sys.argv[1]
    else:
        raise ValueError("Invalid board name argument; valid names are "
                         "day/week/month")
else:
    if os.environ['board_name']:
        if os.environ['board_name'] in helpers.name_associations.keys():
            board_name = os.environ['board_name']
        else:
            raise ValueError("Invalid board name argument; valid names are "
                             "day/week/month")
    else:
        raise TypeError("Missing required board name argument; valid names are "
                        "day/week/month")

# create reddit object for submitting board
reddit = praw.Reddit(client_id=secret.client_id,
                     client_secret=secret.client_secret,
                     username=secret.reddit_username,
                     password=secret.reddit_password,
                     user_agent="TagPro Leaderboards https://github.com/xgi/tagpro-leaderboards")
subreddit = reddit.subreddit('tagpro')

# get the main boards page with links to profiles
response = requests.get("%s/boards" % BASE_URL)

soup = BeautifulSoup(response.text, 'html.parser')

# extract data table
container_div = soup.find('div', attrs={
    'id': 'board-%s' % board_name.title()
})
table = container_div.find('table')
rows = table.find_all('tr')

profile_ids = []
profile_points = {}
for row in rows[1:]:
    profile_id = row.find('a').attrs['href'].split('/profile/')[1]
    profile_ids.append(profile_id)
    profile_points[profile_id] = int(row.find_all('td')[-1].text.strip())

response = requests.get("%s/profiles/%s" % (BASE_URL, ",".join(profile_ids)))
data = response.json()

profiles = []
for player_data in data:
    # create profile obj
    player_id = player_data['_id']
    reserved_name = player_data['reservedName']
    profile = Profile(
        reserved_name.replace('|', '&#124;') if reserved_name is not None
        else "*[unreserved]*",
        player_id,
        profile_points[player_id]
    )

    # parse data into profile obj
    profile.parse_data(player_data)

    # add profile obj to list
    profiles.append(profile)

# sort profiles by points
profiles.sort(
    key=lambda profile: int(profile.points),
    reverse=True
)

# build reddit post
post_text = "|\#|Name|Points|Time|Win%|G|W|L|Pup%|Save%|Tags|Popped|Grabs|Caps|Hold|Prevent|Returns|Support|DCs|\n" +\
            "|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|"""

rank = 1

for profile in profiles:
    name = profile.name

    # add link to profile for top 10 players
    if rank <= 10:
        name = "[%s](http://tagpro-test.koalabeast.com/profile/%s)" % (
            profile.name,
            profile.id
        )

        # make name bold for top 3 players (winners)
        if rank <= 3:
            name = "**%s**" % name

    post_text += "\n|%d|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|" % (
        rank,
        name,
        profile.points,
        profile.data['Time Played'][board_name],
        profile.data['Win %'][board_name],
        profile.data['Games'][board_name],
        profile.data['Wins'][board_name],
        profile.data['Losses'][board_name],
        profile.data['Power-up %'][board_name],
        profile.data['Save %'][board_name],
        profile.data['Tags'][board_name],
        profile.data['Popped'][board_name],
        profile.data['Grabs'][board_name],
        profile.data['Captures'][board_name],
        profile.data['Hold'][board_name],
        profile.data['Prevent'][board_name],
        profile.data['Returns'][board_name],
        profile.data['Support'][board_name],
        profile.data['Disconnects'][board_name]
    )

    rank += 1

cur_date = datetime.utcnow().date()
dynamodb = boto3.resource('dynamodb', region_name=secret.dynamodb_region)
table = dynamodb.Table(secret.dynamodb_name)

submission = None
if board_name == "day":
    # create locked post on our user page
    user_page = reddit.subreddit('u_%s' % secret.reddit_username)
    submission = user_page.submit(
        helpers.submission_title(cur_date, board_name), post_text)
    submission.mod.lock()
elif board_name == "week":
    # create post with weekly info, then create comments for days
    submission = subreddit.submit(
        helpers.submission_title(cur_date, board_name), post_text)
    reply = ""
    for i in range(7):
        date = cur_date - relativedelta(days=i)
        try:
            response = table.get_item(Key={
                'timestamp': date.isoformat(),
                'type': 'day'
            })
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            if 'Item' in response:
                item = response['Item']
                reply += "[%s](%s)\n\n" % (
                    helpers.submission_title(date, "day"),
                    item['url']
                )
    submission.reply(reply)
elif board_name == "month":
    # create post with monthly info
    subreddit.submit(helpers.submission_title(cur_date, board_name), post_text)

# regardless of the type of board, we save it in the database
if submission:
    response = table.put_item(Item={
        'url': submission.url,
        'timestamp': cur_date.isoformat(),
        'type': board_name
    })
