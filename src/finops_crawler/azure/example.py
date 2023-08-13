import datetime
from common import credentials_provider
from finops_crawler import azure

credentials = credentials_provider()

tenant_id, client_id, client_secret = credentials.get_credentials('azure')
azure_costs_client = azure.costs_api(tenant_id, client_id, client_secret)

# Get all subscription ids
subscription_ids = azure_costs_client.get_all_subscriptions()

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

# Fetch cost and usage data for each subscription
for subscription_id in subscription_ids:
    print(f"Subscription_id: {subscription_id}")

    # cost_data = azure_costs_client.get_cost(subscription_id, seven_days_ago, today)
    cost_data = azure_costs_client.get_cost_detailed(subscription_id, seven_days_ago, today)
    print(cost_data)
