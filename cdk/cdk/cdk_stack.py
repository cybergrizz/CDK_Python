from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_ec2 as ec2,
    aws_elasticloadbalancing as elb,
    aws_vpclattice as vpc

)


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        myBucket = s3.Bucket(
            self,
            id="Bucket",
            public_read_access=True,
            website_index_document="index.html",
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            )
            
        )

        myLB = elb.LoadBalancer(
            self,
            vpc=vpc,
            internet_facing=True
        )

        myInstance = ec2.Instance(
            self,
            id="testInstance",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2)
        )

        s3_deployment.BucketDeployment(
            self,
            id="bucketDeployment",
            sources=[s3_deployment.Source.asset("../frontend/djg")],
            destination_bucket=myBucket
        )
