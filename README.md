# Steganography Python Client
## SIIT CSS453 Final Project

## Setup
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
     - `AWS_REGION`  : AWS region such as `"ap-southeast-1"`
## Running
To run the program, simply go into the directory with `cd` and run the `main.py` file. **The server should be running for the program to work**


## Additionals
If you wan to query data to Azure SQL database as well (for testing purposes), add these keys and values to the `.env` file:
- `AZURE_SERVER`
- `AZURE_DATABASE`
- `AZURE_USERNAME`
- `AZURE_PASSWORD`
- `AZURE_DRIVER="{ODBC Driver 17 for SQL Server}"`
    