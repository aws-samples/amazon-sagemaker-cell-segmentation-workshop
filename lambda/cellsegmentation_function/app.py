# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import urllib.parse
import os
import logging

# Import packages from our Lambda layer
from PIL import Image
import boto3
import numpy as np

# Set tmp dir
os.environ['MPLCONFIGDIR'] = "/tmp/"
import matplotlib.pyplot as plt

# The name of the endpoint. The name must be unique within an AWS Region in your AWS account.
ENDPOINT_NAME=os.getenv("ENDPOINT_NAME")

# Specify the region of the SageMaker endpoint
REGION_NAME=os.getenv("REGION_NAME")
    
# Resize images to 512x512x1 for our trained U-net model
IMG_HEIGHT = 512
IMG_WIDTH = 512
IMG_CHANNELS = 1

def app():
    print("Loading cell-segmentation application")

def lambda_handler(event, context):
    print("Received S3 event: " + json.dumps(event, indent=2))

    s3 = boto3.client("s3")

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
    except:
        logging.error("Could not retrieve {}".format(key))
        return False
        
    print("Image Content-Type: " + response['ContentType'])

    cell_image = Image.open(response['Body'])

    # Resize the input to the required 512x512
    newsize = (512, 512)
    cell_image = cell_image.resize(newsize)

    # Show the image for debugging
    #plt.imshow(cell_image)

    # convert to np array, required for our SageMaker inference endpoint
    cell_image = np.array(cell_image)
    
    # Add the additional channel (512x512x1)
    cell_image = np.expand_dims(cell_image, axis=-1)

    print("Processing new image => ", type(cell_image), cell_image.shape)

    # Create a client representing Amazon SageMaker Runtime
    sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=REGION_NAME)
    
    # Submit the image to our SageMaker inference endpoint
    data = json.dumps({'input_1': cell_image.tolist()})

    try:
        response = sagemaker_runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                               ContentType='application/json',
                               Body=data)
    except:
        logging.error("Could not invoke SageMaker endpoint {}".format(ENDPOINT_NAME))

        return False

    result = json.loads(response['Body'].read().decode())
    res = result['predictions']

    print("Successfully processed image")
    # Convert output to numpy
    arr = np.array(res)

    # Filter out any data over the desired threshold
    preds_test_thresh = (arr >= 0.5).astype(np.uint8)

    # Retrieve the image mask
    output = preds_test_thresh[0, :, :, 0]

    # Write the image to our temp volume
    tmp_file = "/tmp/{}".format(os.path.basename(key))

    # Convert to grayscale
    plt.imshow(output, cmap='gray')
    plt.savefig(tmp_file)

    file_output = "output/{}".format(os.path.basename(key))

    print("Cell segmentation mask saved to => ", file_output)

    # Save the mask to S3
    try:
        response = s3.upload_file(tmp_file, bucket, file_output)
    except:
        logging.error("Could not write file to S3 s3://{}/{}".format(bucket, file_output))
        return False
        
    # Return true on success
    return True
