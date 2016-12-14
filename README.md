TagPro Leaderboards Mini
---

TagPro Leaderboards Mini is a script for retrieving leaderboard statistics from the online game TagPro, and posting those stats to the TagPro subreddit. It is intended to be run as a cronjob. This project is a derivative of, and deprecates, [TagPro Leaderboards](https://github.com/xgi/tagpro-leaderboards).

Configuration
---

It is required to create a file named `secret.py` which contains variables for the submitter's Reddit username and password. For example:

```
reddit_username = "TagProLeaderboards"
reddit_password = "hunter2"
```

You can modify the servers the bot will retrieve data from by modifying the variable `servers` in `leaderboards.py`. You should choose servers close to the location of your own, but the more the better (reduces load on the TagPro website).



Usage
---

The script requires an argument containing the name of the board to retrieve:

`leaderboards.py <day/week/month>`

The script is intended to be run as a cronjob/equivalent, and run separately even if boards are resetting simultaneously. This is an example crontab for starting 5 minutes before the boards are scheduled to reset (based on UTC):

```
55 19 * * * * /path/to/leaderboards.py
55 19 * * 7 * /path/to/leaderboards.py
55 19 1 * * * /path/to/leaderboards.py
```
