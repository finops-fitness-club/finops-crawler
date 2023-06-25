import os
import datetime
from finops_crawler import azure, aws
from dotenv import load_dotenv
# from data_storage.postgres_storage import PostgresStorage

load_dotenv()

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

def test_azure():
    # Create an instance of AzureAPI
    tenant_id = os.getenv('AZURE_TENANT_ID')
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    azure_costs_client = azure.costs_api(tenant_id, client_id, client_secret)

    # Get all subscription ids
    subscription_ids = azure_costs_client.get_all_subscriptions()
    # Get the current date (without time)

    # Fetch and store cost and usage data for each subscription
    for subscription_id in subscription_ids:
        print(f"subscription_id: {subscription_id}")

        # subscription_type = azure_costs_client.get_subscription_type(subscription_id)
        # print(f"subscription_type: {subscription_type}")

        cost_data = azure_costs_client.get_cost(subscription_id, seven_days_ago, today)
        print(cost_data)
        # postgres_storage = PostgresStorage()
        # postgres_storage.store_cost_data(cost_data)

def test_aws():
    # Create an instance of AzureAPI
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_costs_client = aws.costs_api(aws_access_key_id, aws_secret_access_key)
    accounts = []
    accounts.append(aws_costs_client.get_account_info())
    org_accounts = aws_costs_client.get_all_accounts()
    if org_accounts:
        accounts += org_accounts
    print(accounts)
    cost_data = aws_costs_client.get_cost(seven_days_ago, today)
    print(cost_data)

def main(source: str):
    if source == 'azure':
        test_azure()
    elif source == 'aws':
        test_aws()
    else:
        print("unknown source")


if __name__ == "__main__":
    main('aws')
