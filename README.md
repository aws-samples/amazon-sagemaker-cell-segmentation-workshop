# Biological Cell Segmentation using Amazon SageMaker

> Please see the AWS Workshop for a complete end-to-end tutorial on using this repository. https://catalog.us-east-1.prod.workshops.aws/workshops/7fb985db-2c2c-4f72-8aa6-7a1c8202b61a

This workshop outlines a machine-learning cell segmentation architecture from scratch for the life-sciences vertical. The use-case is tailored towards having a particular cell of interest from the lab (e.g human embryos, hepatocytes cells, etc) and wish to determine the number of cells, density and basic characteristics of the sample from a microscopy image.

The workshop is expected to take *3 hours*, aimed at individuals who want to learn how Machine Learning can help make predications based on open data. No specific background knowledge is required. The workshop provides step-by-step instructions along with the code required to run each step to cover the following:

* Downloading the dataset from the Broad Bioimage Benchmark Collection (BBBC005) which will be used for training purposes to build our model.
* Demonstrate the process to use a SageMaker Notebook to train a model form scratch, specifically for cell-segmentation.
* Setting up an SageMaker Inference endpoint to host our model.
* Configuring S3 with event notifications, which will trigger a Lambda function which will invoke our SageMaker inference endpoint for processing an image to determine the cell segmentation.

The aim of the workshop is to introduce building a model from scratch and how to use Amazon SageMaker to train and host a model, using a serverless architecture for processing images uploaded to an S3 bucket which interface with a SageMaker inference endpoint.

## Training architecture

The architecture for training the model consists of the following:

![Training](/static/training.png)

## Inference architecture

The architecture for running inference consists of the following:

![Inference](/static/inference-v1.png)

## Next steps

Please see the AWS Workshop for a complete tutorial on using this repository. 

https://catalog.us-east-1.prod.workshops.aws/workshops/7fb985db-2c2c-4f72-8aa6-7a1c8202b61a

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.