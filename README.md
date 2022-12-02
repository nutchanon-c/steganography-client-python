# SIIT CSS453 Final Project: Steganography Python Client

- [SIIT CSS453 Final Project: Steganography Python Client](#siit-css453-final-project-steganography-python-client)
  - [System Requirements](#system-requirements)
  - [Setup](#setup)
  - [Running](#running)
  - [Attributes for ABE](#attributes-for-abe)
  - [Generating CP-ABE Keys](#generating-cp-abe-keys)
  - [Additionals](#additionals)
  - [Performance Testing](#performance-testing)

## System Requirements

Python 3.10.6

Node 16.13.0

Run on Ubuntu or Linux Operating Systems

## Setup

**CP-ABE needs to be installed beforehand. Please refer to [this link](https://acsc.cs.utexas.edu/)**

1. Installing Packages

   1. Python Packages
      - To be able to run the code, you need to install the Python packages in `requirements.txt` file. You can run `pip install -r requirements.txt` to install the packages.
   2. Installing Javascript Packages
      - You can run `yarn` (for yarn) or `npm install` (for npm) or any package manager of your preference.

2. Configure the environmental variables
   - Create a file called `.env` in the root directory with the following keys and values:
     - `API_MASTER_URL` : the endpoint for the API server
     - `AWS_ACCESS_KEY_ID` : AWS Access Key ID
     - `AWS_SECRET_ACCESS_KEY` : AWS Secret Access Key
     - `AWS_BUCKET_NAME` : AWS Bucket Name for the S3 Storage
     - `AWS_REGION` : AWS region such as `"ap-southeast-1"`

## Running

To run the program, simply go into the directory with `cd` and run the `main.py` file. **The server should be running for the program to work**

## Attributes for ABE

Currently, the attribute is fixed for testing purposes, but you can change the attribute(s) in `line 132` in `main.py`. If you want to use a different attribute, you would need to generate a new ABE key and change the key path on `line 304` in `main.py` as well.

## Generating CP-ABE Keys

Please refer to [this link](https://acsc.cs.utexas.edu/cpabe/tutorial.html) for tutorial.

## Additionals

If you wan to query data to Azure SQL database as well (for testing purposes), add these keys and values to the `.env` file:

- `AZURE_SERVER`
- `AZURE_DATABASE`
- `AZURE_USERNAME`
- `AZURE_PASSWORD`
- `AZURE_DRIVER="{ODBC Driver 17 for SQL Server}"`


## Performance Testing
For performance testing, you can use the branch `perf-test` to do so.
