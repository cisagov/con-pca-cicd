"""
Image Views.

This handles the api for all the Image urls.
"""
# Standard Python Libraries
import logging
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime

# Third-Party Libraries
from api.utils.db_utils import (
    delete_single,
    get_list,
    get_single,
    save_single,
    update_single,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class ImageView(APIView):
    """
    This is the ImageView APIView.

    This handles the API for managing images.
    """

    @swagger_auto_schema(
        responses={"200": "Image OK", "400": "Bad Request"},
        security=[],
        operation_id="Single Image",
        operation_description="This handles the operation to upload a single image",
    )
    def post(self, request, format=None):
        """Post method."""
        url = os.environ.get("AWS_ENDPOINT_URL")
        aws_image_bucket = os.environ.get("AWS_STORAGE_BUCKET_IMAGES_NAME")       
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")       
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")    
        aws_region = os.environ.get("AWS_S3_REGION_NAME")    
        session = boto3.session.Session()
        s3_client = session.client(
            service_name='s3',
            endpoint_url=url,
            use_ssl=False,
            aws_access_key_id=aws_image_bucket,
            aws_secret_access_key=aws_access_key_id,
            region_name= aws_region,
        )
        # TODO - Use signed in user's name as additional image saveName attribute
        now = datetime.today()
        saveName = f"Image-{now}.png"        
        try:
            response = s3_client.upload_fileobj(request.data['file'],aws_image_bucket,saveName)
        except ClientError as e:
            print(e)    
            return False
        getURL = f"{url}/{aws_image_bucket}/{saveName}"

        # // get signed url method. Used for generating a signed image url against a s3 bucket with limited permission
        # getURL = s3_client.generate_presigned_url(
        #     ClientMethod='get_object',
        #     ExpiresIn360,
        #     Params={
        #         'Bucket': aws_image_bucket,
        #         'Key': key
        #     }
        # )

        #Replace the url for local stack container location with local host
        #Required so that docker containers can communincate with one another but still allow
        #the tester to retreive the image on there local machine
        getURL = getURL.replace("host.docker.internal","localhost")
        result = { 
            "status": "true", 
            "originalName":"photo_2019-09-18_14-50-27.jpg", 
            "extension":".jpg", 
            "generatedName":"51e8789c-ce47-4828-aeaf-d3a7711fbf6e", 
            "msg":"Image upload successful", 
            "imageUrl":getURL }
        
        return Response(result,status=status.HTTP_201_CREATED)
