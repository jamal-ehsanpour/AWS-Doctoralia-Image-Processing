from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_lambda_event_sources as event_sources,
)
from constructs import Construct

class RekognitionImageAnalysisStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 1. Create S3 bucket for images
        bucket = s3.Bucket(
            self, "DoctoraliaImagesBucket",
            bucket_name="doctoralia-images",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # 2. Create DynamoDB table for results
        results_table = dynamodb.Table(
            self, "ImageAnalysisResults",
            table_name="DoctoraliaImageAnalysis",
            partition_key=dynamodb.Attribute(
                name="image_name",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # 3. Create Lambda function
        rekognition_lambda = lambda_.Function(
            self, "ImageAnalysisFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset("lambda"),
            handler="index.handler",
            environment={
                "RESULTS_TABLE_NAME": results_table.table_name
            }
        )

        # 4. Grant permissions
        bucket.grant_read(rekognition_lambda)
        results_table.grant_write_data(rekognition_lambda)
        rekognition_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["rekognition:DetectFaces"],
                resources=["*"]
            )
        )

        # 5. Add S3 trigger
        rekognition_lambda.add_event_source(
            event_sources.S3EventSource(
                bucket,
                events=[s3.EventType.OBJECT_CREATED],
                filters=[s3.NotificationKeyFilter(prefix="Images/")]
            )
        )

        # Outputs
        self.bucket_name = bucket.bucket_name
        self.table_name = results_table.table_name