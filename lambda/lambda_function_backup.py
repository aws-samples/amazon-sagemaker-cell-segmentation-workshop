# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import urllib.parse
import boto3
import numpy

from skimage.io import imread, imshow
from skimage.transform import resize

IMG_HEIGHT = 512
IMG_WIDTH = 512
IMG_CHANNELS = 1

s3 = boto3("s3")

print('Loading function')

def app():
    print("Loading app")
    
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        
        bkt = s3.Bucket('sentinel-s2-l1c')
        object = bkt.Object('tiles/10/S/DG/2015/12/7/0/B01.jp2')

        file_stream = io.StringIO()
        object.download_fileobj(file_stream)

        # read the image using skimage
        image = imread(file_stream)
    
        # resize the image
        image = resize(image, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
    
        # use np.expand dims to add a channel axis so the shape becomes (IMG_HEIGHT, IMG_WIDTH, 1)
        image = numpy.expand_dims(image, axis=-1)
        
        # Create a low-level client representing Amazon SageMaker Runtime
        sagemaker_runtime = boto3.client("sagemaker-runtime", region_name="ap-southeast-2")

        # The name of the endpoint. The name must be unique within an AWS Region in your AWS account. 
        endpoint_name='tensorflow-inference-2023-03-01-06-49-33-474'

        data = json.dumps({'input_3': image_data.tolist()})

        response = sagemaker_runtime.invoke_endpoint(EndpointName=endpoint_name,
                                   ContentType='application/json',
                                   Body=data)
        result = json.loads(response['Body'].read().decode())
        res = result['predictions']
        
        print(res)
        
        return res
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e