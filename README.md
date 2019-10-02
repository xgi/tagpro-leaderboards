# TagPro Leaderboards

TagPro Leaderboards is a script for retrieving leaderboard statistics from the online game TagPro, and posting those stats to the TagPro subreddit. It is intended to be run on [AWS Lambda](https://aws.amazon.com/lambda/).

## Configuration

### Reddit

1. [Register a Reddit application.](https://github.com/reddit/reddit/wiki/OAuth2#getting-started) You should use the "script" classification.

2. Identify the client_id and client_secret keys from the app's information panel.

3. Create a file named `secret.py` in the same directory as `leaderboards.py` and fill it with the following variables:

```python
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
reddit_username = "YOUR_REDDIT_USERNAME"
reddit_password = "YOUR_REDDIT_PASSWORD"
dynamodb_name = "YOUR_DYNAMODB_TABLE_NAME"
dynamodb_region = "YOUR_DYNAMODB_TABLE_REGION"
```

### AWS

From the [AWS Console](https://aws.amazon.com/console/):

1. Create a Lambda function.
    * Choose Python 3.7 as the runtime.
    * Upload the project directory as the source. The entrypoint is `leaderboards.py`.
    * \>= 512MB memory allocation is preferred for quick execution.
2. Create 3 CloudWatch rules.
    * Set a "Schedule" pattern with Cron expression:
        * daily: `59 19 * * ? *`
        * weekly: `59 19 ? * 1 *`
        * monthly: `59 19 1 * ? *`
    * Set the target as the lambda function.
    * As input to the function, add JSON text `{"board_name":"<value>"}` where `value` is day/week/month.
3. Create a DynamoDB table.
    * The partition key is a string called `timestamp`.
    * The sort key is a string called `type`.
    * Ensure the role for the Lambda function has the ability to read/write this table.

The Lambda console lets you test execute the script. Make use of it!

## Usage

The script requires an argument containing the name of the board to retrieve:

`leaderboards.py <day/week/month>`

Alternatively, it can be run with the `board_name` environment variable set to one of the above values.

The script is intended to be executed separately even if boards are resetting simultaneously. For example, it is run three times on a day where both a weekly and monthly board reset (since the daily board resets every day).
