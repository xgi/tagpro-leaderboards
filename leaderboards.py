#!/bin/python

import praw
from bs4 import BeautifulSoup
import requests
import sys
import os
import random

# local modules
import secret
import helpers
from profile import Profile


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

# list of servers to retrieve data from
servers = ['test']

# create reddit object for submitting board
reddit = praw.Reddit(client_id=secret.client_id,
                     client_secret=secret.client_secret,
                     username=secret.reddit_username,
                     password=secret.reddit_password,
                     user_agent="TagPro Leaderboards https://github.com/xgi/tagpro-leaderboards")
subreddit = reddit.subreddit('tagpro')

## get the main boards page with links to profiles
# request boards page and rotate the server list
response = helpers.request(servers, '/boards')
servers = helpers.rotate(servers)

soup = BeautifulSoup(response.text, 'html.parser')

# extract data table
container_div = soup.find('div', attrs={
    'id': 'board-%s' % board_name.title()
})
table = container_div.find('table')
rows = table.find_all('tr')

# create list of profile links by extracting the a element of each row
profile_links = [row.find('a') for row in rows[1:]]

## retrieve individual profile information
profiles = []

for link in profile_links:
    # retrieve and sanitize profile name
    name = link.text.strip()
    name = name.replace('|','&#124;')

    # create profile obj
    profile = Profile(link.attrs['href'], name)

    # request profile page and rotate the server list
    response = helpers.request(servers, profile.url)
    servers = helpers.rotate(servers)

    soup = BeautifulSoup(response.text, "html.parser")

    # extract data table
    container_div = soup.find('div', attrs={
        'id': 'all-stats'
    })
    table = container_div.find('table')

    # parse table data into profile obj
    profile.read_table(table)

    # add profile obj to list
    profiles.append(profile)

# re-sort profiles by points because they may have changed in the time it took
# to download all profiles
profiles.sort(
    key=lambda profile: int(profile.data['Points'][board_name]),
    reverse=True
)

## build reddit post
post_text = \
"""|\#|Name|Points|Time|Win%|G|W|L|Pup%|Save%|Tags|Popped|Grabs|Caps|Hold|Prevent|Returns|Support|DCs|
:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|"""

rank = 1

for profile in profiles:
    name = profile.name

    # add link to profile for top 10 players
    if rank <= 10:
        name = "[%s](http://tagpro-radius.koalabeast.com%s)" % (
            profile.name,
            profile.url
        )

        # make name bold for top 3 players (winners)
        if rank <= 3:
            name = "**%s**" % name

    post_text += "\n|%d|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|" % (
        rank,
        name,
        profile.data['Points'][board_name],
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

subreddit.submit(helpers.submission_title(board_name), post_text)
