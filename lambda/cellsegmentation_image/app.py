# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# v2 implementation using a container - WIP
import sys
import boto3
import numpy as np
import json
import urllib.parse
import os
import logging

from PIL import Image
from io import StringIO

def handler(event, context):
    return 'Hello from AWS Lambda using Python' + sys.version + '!'