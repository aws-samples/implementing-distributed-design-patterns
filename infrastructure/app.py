#!/usr/bin/env python3
import os

import aws_cdk as cdk

from application_stack import ApplicationStack
from campaign.CampaignStack import CampaignStack
from point.PointStack import PointStack
from retail.RetailStack import RetailStack

app = cdk.App()

env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
)

point_stack = PointStack(
    app,
    "PointStack",
    env=env,
)

campaign_stack = CampaignStack(
    app,
    "CampaignStack",
    point_command_lambda=point_stack.point_command_lambda,
    env=env,
)

retail_stack = RetailStack(
    app,
    "RetailStack",
    env=env,
)

ApplicationStack(
    app,
    "ApplicationStack",
    point_command_lambda=point_stack.point_command_lambda,
    point_query_lambda=point_stack.point_query_lambda,
    rules_processor_lambda=campaign_stack.rules_processor_lambda,
    campaign_get_campaign_rule_lambda=campaign_stack.campaign_get_campaign_rule_lambda,
    campaign_get_campaign_rules_lambda=campaign_stack.campaign_get_campaign_rules_lambda,
    campaign_create_campaign_rule_lambda=campaign_stack.campaign_create_campaign_rule_lambda,
    campaign_update_campaign_rule_lambda=campaign_stack.campaign_update_campaign_rule_lambda,
    campaign_delete_campaign_rule_lambda=campaign_stack.campaign_delete_campaign_rule_lambda,
    retail_get_user_wallet_lambda=retail_stack.retail_get_user_wallet_lambda,
    retail_get_product_lambda=retail_stack.retail_get_product_lambda,
    retail_process_purchase_lambda=retail_stack.retail_process_purchase_lambda,
    central_bus=retail_stack.central_bus,
    env=env,
)

app.synth()
