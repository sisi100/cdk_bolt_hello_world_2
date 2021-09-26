import os

from aws_cdk import core
from aws_cdk.aws_apigateway import LambdaIntegration, RestApi
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_lambda_python import PythonFunction
from aws_cdk.aws_ssm import StringListParameter

APP_NAME = "CdkBoltHelloWorld"
SSM_PARAMETER_NAMES = ["/cdk_bolt_hello_world/slack_bot_token", "/cdk_bolt_hello_world/slack_signing_secret"]


class CdkBoltHelloWorldStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_ = PythonFunction(
            self, f"{APP_NAME}Lambda", entry="cdk_bolt_hello_world", handler="handler", runtime=Runtime.PYTHON_3_8,
        )

        api = RestApi(self, f"{APP_NAME}Api")
        api.root.add_method("POST", LambdaIntegration(lambda_))

        for param_name in SSM_PARAMETER_NAMES:
            StringListParameter.from_string_list_parameter_name(
                self, f"{APP_NAME}-{param_name}", param_name
            ).grant_read(lambda_)


app = core.App()
env = core.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION"))
CdkBoltHelloWorldStack(app, APP_NAME, env=env)
app.synth()
