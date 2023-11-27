from aws_cdk import (
    Stack,
    aws_lambda as lda,
    aws_dynamodb as ddb,
    Duration,
)
from constructs import Construct


class PointStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        #
        # DynamoDB
        #
        point_transaction_table = ddb.TableV2(
            self,
            "PointTransactionTable",
            table_name="PointTransactionTable",
            billing=ddb.Billing.on_demand(),
            dynamo_stream=ddb.StreamViewType.NEW_AND_OLD_IMAGES,
            partition_key={"name": "id", "type": ddb.AttributeType.STRING},
        )

        daily_balance_table = ddb.TableV2(
            self,
            "DailyBalanceTable",
            table_name="DailyBalanceTable",
            billing=ddb.Billing.on_demand(),
            partition_key={"name": "account_id", "type": ddb.AttributeType.STRING},
            sort_key={"name": "issued_date", "type": ddb.AttributeType.STRING},
        )

        #
        # Lambda
        #
        POINT_TTL = "2"

        self.point_command_lambda = lda.Function(
            self,
            "PointCommandHandler",
            function_name="PointCommandHandler",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset("../application/lambdas/points"),
            handler="handlers.command_handler.handle_request",
            environment={
                "POINT_TRANSACTION_TABLE": point_transaction_table.table_name,
                "DAILY_BALANCE_TABLE": daily_balance_table.table_name,
                "POINT_TTL": POINT_TTL,
            },
        )

        daily_balance_projection_lambda = lda.Function(
            self,
            "DailyBalanceProjectionEngine",
            function_name="DailyBalanceProjectionEngine",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset("../application/lambdas/points"),
            handler="handlers.daily_balance_projection_handler.handle_records",
            timeout=Duration.seconds(30),
            environment={
                "DAILY_BALANCE_TABLE": daily_balance_table.table_name,
                "POINT_TTL": POINT_TTL,
            },
        )

        self.point_query_lambda = lda.Function(
            self,
            "PointQueryHandler",
            function_name="PointQueryHandler",
            runtime=lda.Runtime.PYTHON_3_11,
            architecture=lda.Architecture.ARM_64,
            code=lda.Code.from_asset("../application/lambdas/points"),
            handler="handlers.query_handler.handle_request",
            environment={
                "DAILY_BALANCE_TABLE": daily_balance_table.table_name,
                "POINT_TTL": POINT_TTL,
            },
        )

        lambda_trigger = lda.CfnEventSourceMapping(
            self,
            "PointTransactionStreamTrigger",
            function_name=daily_balance_projection_lambda.function_name,
            batch_size=20,
            maximum_batching_window_in_seconds=5,
            event_source_arn=point_transaction_table.table_stream_arn,
            starting_position="TRIM_HORIZON",
        )

        #
        # Permission
        #
        point_transaction_table.grant_read_write_data(self.point_command_lambda)
        point_transaction_table.grant_read_write_data(daily_balance_projection_lambda)
        point_transaction_table.grant_stream_read(daily_balance_projection_lambda)

        daily_balance_table.grant_read_write_data(daily_balance_projection_lambda)
        daily_balance_table.grant_read_data(self.point_command_lambda)
        daily_balance_table.grant_read_data(self.point_query_lambda)
