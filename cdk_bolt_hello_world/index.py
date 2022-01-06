import boto3
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler


def make_app():
    ssm = boto3.client("ssm")
    slack_bot_token, slack_signing_secret = (
        ssm.get_parameter(Name=f"/cdk_bolt_hello_world/{name}", WithDecryption=True)["Parameter"]["Value"]
        for name in ["slack_bot_token", "slack_signing_secret"]
    )
    return App(
        signing_secret=slack_signing_secret,
        token=slack_bot_token,
        process_before_response=True,  # 同期処理にする（デフォルトは非同期）
    )


app = make_app()


@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")


def handler(event, context):
    return SlackRequestHandler(app).handle(event, context)
