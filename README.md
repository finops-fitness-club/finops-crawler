# finops-crawler

## Basic Usage

This script is designed to fetch cost data from both Azure and AWS platforms. To use it, follow the steps below:

### Setting up the Environment

Before you start, you'll need to set up your environment variables with the necessary credentials. 

For Azure:

- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`

And for AWS:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

We recommend using the dotenv module to manage your environment variables. Create a `.env` file in your project directory and add your credentials:

```env
AZURE_TENANT_ID=your_azure_tenant_id
AZURE_CLIENT_ID=your_azure_client_id
AZURE_CLIENT_SECRET=your_azure_client_secret
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
```

### Running the Script

To run the script, simply call the main() function at the end of the script and pass in the source you'd like to fetch data from, either 'azure' or 'aws'.

```
if __name__ == "__main__":
    main('aws')  # or 'azure'
```

### Fetching Azure Data

When fetching Azure data, the script will create an instance of AzureAPI using the credentials you provided. It will then fetch all subscription ids for the Azure account and fetch and print cost data for each subscription over the past seven days.

### Fetching AWS Data

When fetching AWS data, the script will create an instance of AWSAPI using the credentials you provided. It will fetch the current account info and all organization accounts (if any). It will then fetch and print cost and usage data over the past seven days.