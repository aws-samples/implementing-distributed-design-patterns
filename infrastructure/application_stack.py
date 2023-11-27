from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_lambda as lda,
    aws_events as events,
    aws_events_targets as targets,
    aws_sqs as sqs,
    CfnOutput,
)
from constructs import Construct


class ApplicationStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        point_command_lambda: lda.Function,
        point_query_lambda: lda.Function,
        rules_processor_lambda: lda.Function,
        campaign_get_campaign_rule_lambda: lda.Function,
        campaign_get_campaign_rules_lambda: lda.Function,
        campaign_create_campaign_rule_lambda: lda.Function,
        campaign_update_campaign_rule_lambda: lda.Function,
        campaign_delete_campaign_rule_lambda: lda.Function,
        retail_get_user_wallet_lambda: lda.Function,
        retail_get_product_lambda: lda.Function,
        retail_process_purchase_lambda: lda.Function,
        central_bus: events.EventBus,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # API Gateway Endpoint and Resources
        api = apigw.RestApi(
            self,
            "PointSystemAPI",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            ),
        )

        api.root.add_resource("purchase").add_method(
            "POST",
            apigw.LambdaIntegration(retail_process_purchase_lambda),
        )

        products = api.root.add_resource("products")
        products_path = products.add_resource("{id}")
        products_path.add_method(
            "GET", apigw.LambdaIntegration(retail_get_product_lambda)
        )

        users = api.root.add_resource("users")
        balance = users.add_resource("balance")
        balance_path = balance.add_resource("{username}")
        balance_path.add_method(
            "GET", apigw.LambdaIntegration(retail_get_user_wallet_lambda)
        )

        items = api.root.add_resource("points")
        items.add_method("POST", apigw.LambdaIntegration(point_command_lambda))
        items.add_method("DELETE", apigw.LambdaIntegration(point_command_lambda))
        items.add_method("GET", apigw.LambdaIntegration(point_query_lambda))

        campaigns = api.root.add_resource("campaigns")
        campaigns.add_method(
            "GET",
            apigw.LambdaIntegration(campaign_get_campaign_rules_lambda),
        )
        campaigns.add_method(
            "POST",
            apigw.LambdaIntegration(
                campaign_create_campaign_rule_lambda
            ),
        )

        campaign = campaigns.add_resource("{campaign_name}")
        campaign.add_method(
            "GET",
            apigw.LambdaIntegration(campaign_get_campaign_rule_lambda),
            request_parameters={
                "method.request.path.campaign_name": True,
                "method.request.querystring.client": True,
            },
        )
        campaign.add_method(
            "PATCH",
            apigw.LambdaIntegration(
                campaign_update_campaign_rule_lambda
            ),
            request_parameters={
                "method.request.path.campaign_name": True,
                "method.request.querystring.client": True,
            },
        )
        campaign.add_method(
            "DELETE",
            apigw.LambdaIntegration(
                campaign_delete_campaign_rule_lambda
            ),
            request_parameters={
                "method.request.path.campaign_name": True,
                "method.request.querystring.client": True,
            },
        )

        point_command_lambda.grant_invoke(rules_processor_lambda)

        rule = events.Rule(
            self,
            "rule",
            event_pattern=events.EventPattern(source=["step.functions"]),
            event_bus=central_bus,
        )

        campaign_rules_processor_dlq = sqs.Queue(self, "CampaignRulesProcessorDLQ")
        rule.add_target(
            targets.LambdaFunction(
                rules_processor_lambda,
                dead_letter_queue=campaign_rules_processor_dlq,  # Optional: add a dead letter queue
                retry_attempts=2,
            )
        )

        CfnOutput(self, "API URL", value=api.url)
