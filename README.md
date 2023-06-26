# finops-crawler

This project is active. Development is ongoing, contributions are welcome (see below).

## Basic Usage

This package is designed to fetch cost/usage data from various platforms (Azure, AWS, OpenAI, more to follow).

The result is a Python list of dicts as returned by the API or SDK.

To use it, follow the steps below:

### Setting up the Environment

Before you start, you'll need to set up your environment variables with the necessary credentials for the platforms that you wish to use. For example, to query OpenAI usage then you only need to have the OPENAI_ORG_ID and OPENAI_API_KEY described.

For Azure:

- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`

For AWS:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

For OpenAI:

- `OPENAI_ORG_ID`
- `OPENAI_API_KEY`

We recommend using the dotenv module to manage your environment variables. Create a `.env` file in your project directory and add your credentials:

```env
AZURE_TENANT_ID=your_azure_tenant_id
AZURE_CLIENT_ID=your_azure_client_id
AZURE_CLIENT_SECRET=your_azure_client_secret
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
OPENAI_ORG_ID=your_openai_org_id
OPENAI_API_KEY=your_openai_api_key
```

### Minimum required permissions

More thorough documentation will follow soon, but for now:

- Azure, the service principal requires `Cost Management Reader` permission for each subscription
- AWS, the user requires the following actions in a custom policy: `organizations:DescribeAccount`, `organizations:ListAccounts`, `ce:*`
- OpenAI, nothing specific required

### Getting the cost data

Getting the data depends on the platform. For example, in Azure you will immediately see all subscriptions that you have access to. In AWS, on the other hand, you either are part of an organization or have a standalone account, etc. OpenAI also has organizations system, which is currently ignored by the crawler.

There are examples in [example.py](example.py) file.

*Note*: querying long time periods might trigger paginated results. AWS currently handles it correctly, very soon Azure will as well. Have not tested yet with OpenAI.

### Plans

Increase breath by expanding to various other tools and platforms (Databricks, GCP, etc.)

Increase depth by implementing `save_to_postgres` or similar functionality to actually store it.

### Contributing

Got ideas for improvements? We'd love your input!

1. Fork and clone this repository.
2. Optionally, choose an issue labeled as "help wanted" or "good first issue".
3. Submit a pull request with your changes and a clear description.

Remember, all contributions from bug fixes to documentation updates are greatly appreciated!

Email: finops.fitness.club@gmail.com
