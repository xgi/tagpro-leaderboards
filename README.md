# TagPro Leaderboards

TagPro Leaderboards is a script for retrieving leaderboard statistics from the online game TagPro, and posting those stats to the TagPro subreddit. It is intended to be run as a cronjob, or scheduled on a service such as [AWS Lambda](https://aws.amazon.com/lambda/).

## Configuration

1. [Register a Reddit application.](https://github.com/reddit/reddit/wiki/OAuth2#getting-started) You should use the "script" classification.

2. Identify the client_id and client_secret keys from the app's information panel.

3. Create a file named `secret.py` in the same directory as `leaderboards.py` and fill it with the following variables:

```python
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
reddit_username = "YOUR_REDDIT_USERNAME"
reddit_password = "YOUR_REDDIT_PASSWORD"
```

## Usage

The script requires an argument containing the name of the board to retrieve:

`leaderboards.py <day/week/month>`

The script is intended to be run as a cronjob/equivalent, and run separately even if boards are resetting simultaneously. This is an example crontab for starting 5 minutes before the boards are scheduled to reset (based on UTC):

```text
55 19 * * * /path/to/leaderboards.py day
55 19 * * 0 /path/to/leaderboards.py week
55 19 1 * * /path/to/leaderboards.py month
```
