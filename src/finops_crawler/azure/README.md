# finops-crawler for Azure

[Main documentation](/) about the idea, structure and contribution. It's a package for getting Azure cost data into Python. The group-by dimensions are ResourceId and ChargeType to provide maximum meaningful granularity.

## Setting up the service principal and permissions

### Quickstart

Using [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli). It creates a service principal and assigns the "Cost Management Reader" role to it in your subscription.

Note: `get_cost_detailed()` needs additional permissions, the specific set to be determined (TODO)

```bash
az ad sp create-for-rbac --name "Finops Crawler"
```
outputs:
```json
{
  "appId": "APP_ID_THAT_WAS_JUST_CREATED",
  "displayName": "Finops Crawler",
  "password": "YOUR_APP_PASSWORD",
  "tenant": "YOUR_TENANT_ID"
}
```
Then use `APP_ID_THAT_WAS_JUST_CREATED` like this:
```bash
az role assignment create --assignee APP_ID_THAT_WAS_JUST_CREATED --role "Cost Management Reader" --scope /subscriptions/YOUR_SUBSCRIPTION_ID
```
Then set environment variables (yes, "app" and "client" are the same thing here):
```env
AZURE_TENANT_ID=YOUR_TENANT_ID
AZURE_CLIENT_ID=APP_ID_THAT_WAS_JUST_CREATED
AZURE_CLIENT_SECRET=YOUR_APP_PASSWORD
```


## Long version

The package reads cost and usage data from all the subscriptions that it has access to. There are also subscription offer types that [don't have the cost data available at all](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-acm-cost-analysis#prerequisites), for example, the one you get if you apply for startup credits. [Subscription offer types](https://azure.microsoft.com/en-us/support/legal/offer-details/), full intro to [Azure Cost Management data](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data).

### Step 1 - Create the service principal

The easiest way to have this script authorized to Azure is by creating a service principal and giving it the minimum amount of permissions required. The [documentation](https://learn.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals?tabs=browser) for service principals is thorough and helpful, also showing ways to do it via Azure portal, PowerShell, and Azure CLI. We suggest giving it a descriptive name, like "Finops Crawler".

Registration of the service principal gives you an application ID and a password.

If you do it via the CLI then the result looks like this:
```json
{
  "appId": "APP_ID_THAT_WAS_JUST_CREATED",
  "displayName": "Finops Crawler",
  "password": "YOUR_APP_PASSWORD",
  "tenant": "YOUR_TENANT_ID"
}
```
These will be used later.

### Step 2 - Assign it to a subscription and give it permissions

The second step is to assign it some permissions so that it can read the cost data. It's done via [Role-based access control](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview) (RBAC) that ties together the service principal, the subscription, and the specific permission. The required permission is "Cost Management Reader".

### Step 3 - Environment variables for the script

One should never write credentials directly into code. Thus, there is a way to read it from the environment variables at runtime. This is also how this script expects the credentials.

This is what should exist in your environment variables before running the script. Note that the values come from the output of the first step.
```env
AZURE_TENANT_ID=YOUR_TENANT_ID
AZURE_CLIENT_ID=APP_ID_THAT_WAS_JUST_CREATED
AZURE_CLIENT_SECRET=YOUR_APP_PASSWORD
```

### Step 4 - Use the package

Copy-paste the following code into a Python file and run it (also found in the [example.py](example.py) file).
```python
import datetime
from finops_crawler import azure, credentials_provider

credentials = credentials_provider.api()

azure_costs_client = azure.costs_api(*credentials.get_credentials('azure'))

# Get all subscription ids
subscription_ids = azure_costs_client.get_all_subscriptions()

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

# Fetch cost and usage data for each subscription
for subscription_id in subscription_ids:
    print(f"Subscription_id: {subscription_id}")

    cost_data = azure_costs_client.get_cost(subscription_id, seven_days_ago, today)
    print(cost_data)
```

A successful run results in a list of dicts with the fields `UsageDate`, `ResourceId`, `ChargeType`, `Currency`, and `Cost` (I hope - the API is broken for my test account at the moment).

Enjoy :)

Email: finops.fitness.club@gmail.com
