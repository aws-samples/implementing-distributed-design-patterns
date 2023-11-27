from aws_cdk import (
    Stack,
    aws_lambda as lda,
    aws_dynamodb as ddb,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_cloudfront as cf,
    aws_cloudfront_origins as origins,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_events as events,
    aws_logs as logs,
    CfnOutput,
)
from constructs import Construct

class RetailStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.central_bus = events.EventBus(self, "bus", event_bus_name="CentralBus")

        #
        # DynamoDB
        #
        products_table = ddb.TableV2(
            self,
            "ProductsTable",
            table_name="ProductsTable",
            billing=ddb.Billing.on_demand(),
            partition_key={"name": "id", "type": ddb.AttributeType.STRING},
        )

        user_wallet_balance_table = ddb.TableV2(
            self,
            "UserWalletTable",
            table_name="UserWalletTable",
            billing=ddb.Billing.on_demand(),
            partition_key={"name": "username", "type": ddb.AttributeType.STRING},
        )

        #
        # Lambda
        #
        self.retail_get_product_lambda = lda.Function(
            self,
            "GetProduct",
            function_name="GetProduct",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset("../application/lambdas/retail"),
            handler="handlers.get_product_handler.handle_request",
            environment={
                "PRODUCT_TABLE": products_table.table_name,
            },
        )

        self.retail_get_user_wallet_lambda = lda.Function(
            self,
            "GetUserWallet",
            function_name="GetUserWallet",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset("../application/lambdas/retail"),
            handler="handlers.get_user_wallet_handler.handle_request",
            environment={
                "USER_WALLET_BALANCE_TABLE": user_wallet_balance_table.table_name,
            },
        )

        retail_process_payment_lambda = lda.Function(
            self,
            "ProcessPayment",
            function_name="ProcessPayment",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset("../application/lambdas/retail"),
            handler="handlers.process_payment_handler.handle_request",
            environment={
                "USER_WALLET_BALANCE_TABLE": user_wallet_balance_table.table_name,
                "PRODUCT_TABLE": products_table.table_name,
            },
        )

        retail_reserve_stock_lambda = lda.Function(
            self,
            "ReserveStock",
            function_name="ReserveStock",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset("../application/lambdas/retail"),
            handler="handlers.reserve_stock_handler.handle_request",
            environment={
                "PRODUCT_TABLE": products_table.table_name,
            },
        )

        retail_release_stock_lambda = lda.Function(
            self,
            "ReleaseStock",
            function_name="ReleaseStock",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset("../application/lambdas/retail"),
            handler="handlers.release_stock_handler.handle_request",
            environment={
                "PRODUCT_TABLE": products_table.table_name,
            },
        )

         # Create State Machine for Processing Purchase Request
        reserve_stock_task = tasks.LambdaInvoke(
            self,
            "Step1: Reserve Stock",
            lambda_function=retail_reserve_stock_lambda,
            output_path="$.Payload",
        )

        process_payment_task = tasks.LambdaInvoke(
            self,
            "Step2: Process Payment",
            lambda_function=retail_process_payment_lambda,
            output_path="$.Payload",
        )

        release_stock_task = tasks.LambdaInvoke(
            self,
            "Step1a: Release Stock",
            lambda_function=retail_release_stock_lambda,
            output_path="$.Payload",
        )

        purchase_completed_task = tasks.EventBridgePutEvents(
            self,
            "Step3: Emit an event to Loyalty Domain",
            entries=[
                tasks.EventBridgePutEventsEntry(
                    detail=sfn.TaskInput.from_json_path_at("$"),
                    event_bus=self.central_bus,
                    detail_type="Purchase Completed",
                    source="step.functions",
                )
            ],
            result_path="$.emitEvent",
        )

        not_enough_stock_pass = sfn.Pass(self, "Check out failed: Not enough stock")
        not_enough_balance_pass = sfn.Pass(self, "Check out failed: Not enough balance")
        checkout_completed_pass = sfn.Pass(self, "Check out success")

        check_stock_choices = sfn.Choice(self, "Has enough stock?")
        check_stock_choices.when(
            sfn.Condition.boolean_equals("$.success", True), process_payment_task
        )

        check_payment_status_choice = sfn.Choice(self, "Payment success?")
        check_payment_status_choice.when(
            sfn.Condition.boolean_equals("$.success", True), purchase_completed_task
        )

        process_payment_task.next(check_payment_status_choice)
        purchase_completed_task.next(checkout_completed_pass)

        check_stock_choices.otherwise(not_enough_stock_pass)
        check_payment_status_choice.otherwise(release_stock_task)
        release_stock_task.next(not_enough_balance_pass)

        definition = sfn.DefinitionBody.from_chainable(
            reserve_stock_task.next(check_stock_choices)
        )

        log_group = logs.LogGroup(self, "PurchaseStateMachineLogGroup")
        purchase_state_machine = sfn.StateMachine(
            self,
            "PurchaseStateMachine",
            state_machine_name="PurchaseStateMachine",
            definition_body=definition,
            state_machine_type=sfn.StateMachineType.EXPRESS,
            logs=sfn.LogOptions(
                level=sfn.LogLevel.ALL,
                destination=log_group,
                include_execution_data=True,
            ),
        )

        self.retail_process_purchase_lambda = lda.Function(
            self,
            "ProcessPurchase",
            function_name="ProcessPurchase",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset("../application/lambdas/retail"),
            handler="handlers.process_purchase_handler.handle_request",
            environment={
                "PURCHASE_STATE_MACHINE": purchase_state_machine.state_machine_arn,
            },
        )

        #
        # Front-end
        #
        static_web_bucket = s3.Bucket(
            self,
            "static-web-bucket",
        )

        s3_deployment.BucketDeployment(
            self,
            "s3-static-file-deployment",
            sources=[s3_deployment.Source.asset("../webapp/build")],
            destination_bucket=static_web_bucket,
        )

        cf_dist = cf.Distribution(
            self,
            "static-web-dist",
            default_behavior=cf.BehaviorOptions(
                origin=origins.S3Origin(static_web_bucket),
                response_headers_policy=cf.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS,
            ),
        )

        #
        # Permission
        #
        products_table.grant_read_data(self.retail_get_product_lambda)
        products_table.grant_read_data(retail_process_payment_lambda)
        products_table.grant_read_write_data(retail_reserve_stock_lambda)
        products_table.grant_read_write_data(retail_release_stock_lambda)

        user_wallet_balance_table.grant_read_data(self.retail_get_user_wallet_lambda)
        user_wallet_balance_table.grant_read_write_data(retail_process_payment_lambda)

        purchase_state_machine.grant_start_execution(self.retail_process_purchase_lambda)
        purchase_state_machine.grant_start_sync_execution(self.retail_process_purchase_lambda)

        self.central_bus.grant_put_events_to(purchase_state_machine)

        CfnOutput(self, "Web Distribution URL", value=cf_dist.domain_name)
