from aws_cdk import (
    Stack,
    aws_lambda as lda,
    aws_dynamodb as ddb,
)
from constructs import Construct

class CampaignStack(Stack):
    def __init__(self, scope: Construct, id: str, point_command_lambda: lda.Function, **kwargs):
        super().__init__(scope, id, **kwargs)

        #
        # DynamoDB
        #
        campaign_table = ddb.TableV2(
            self,
            "CampaignTable",
            table_name="CampaignTable",
            billing=ddb.Billing.on_demand(),
            partition_key={"name": "client", "type": ddb.AttributeType.STRING},
            sort_key={"name": "campaign_name", "type": ddb.AttributeType.STRING},
        )

        #
        # Lambda
        #
        self.campaign_get_campaign_rule_lambda = lda.Function(
            self,
            "GetCampaignRule",
            function_name="GetCampaignRule",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset(
                "../application/lambdas/campaign"
            ),
            handler="handlers.get_campaign_rule.lambda_handler",
            environment={
                "CAMPAIGN_TABLE": campaign_table.table_name,
            },
        )

        self.campaign_get_campaign_rules_lambda = lda.Function(
            self,
            "GetCampaignRules",
            function_name="GetCampaignRules",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset(
                "../application/lambdas/campaign"
            ),
            handler="handlers.get_campaign_rules.lambda_handler",
            environment={
                "CAMPAIGN_TABLE": campaign_table.table_name,
            },
        )

        self.campaign_create_campaign_rule_lambda = lda.Function(
            self,
            "CreateCampaignRule",
            function_name="CreateCampaignRule",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset(
                "../application/lambdas/campaign"
            ),
            handler="handlers.create_campaign_rule.lambda_handler",
            environment={
                "CAMPAIGN_TABLE": campaign_table.table_name,
            },
        )

        self.campaign_update_campaign_rule_lambda = lda.Function(
            self,
            "UpdateCampaignRule",
            function_name="UpdateCampaignRule",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset(
                "../application/lambdas/campaign"
            ),
            handler="handlers.update_campaign_rule.lambda_handler",
            environment={
                "CAMPAIGN_TABLE": campaign_table.table_name,
            },
        )

        self.campaign_delete_campaign_rule_lambda = lda.Function(
            self,
            "DeleteCampaignRule",
            function_name="DeleteCampaignRule",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset(
                "../application/lambdas/campaign"
            ),
            handler="handlers.delete_campaign_rule.lambda_handler",
            environment={
                "CAMPAIGN_TABLE": campaign_table.table_name,
            },
        )

        # Rules Engine infrastructure
        self.rules_processor_lambda = lda.Function(
            self,
            "RulesProcessor",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset("../application/lambdas/campaign"),
            handler="handlers.rules_handler.handle_request",
            environment={
                "CAMPAIGN_TABLE": campaign_table.table_name,
                "POINT_FUNCTION": point_command_lambda.function_name,
            },
        )
        
        #
        # Permission
        #
        campaign_table.grant_read_write_data(self.rules_processor_lambda)
        campaign_table.grant_read_data(self.campaign_get_campaign_rule_lambda)
        campaign_table.grant_read_data(self.campaign_get_campaign_rules_lambda)
        campaign_table.grant_read_write_data(self.campaign_create_campaign_rule_lambda)
        campaign_table.grant_read_write_data(self.campaign_update_campaign_rule_lambda)
        campaign_table.grant_read_write_data(self.campaign_delete_campaign_rule_lambda)
        