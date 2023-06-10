import requests
import datetime
import time
from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, QueryDataset

from azure.mgmt.resource import SubscriptionClient

from azure.core.exceptions import ResourceNotFoundError
from azure.core.exceptions import HttpResponseError

from finops_crawler.base import CloudAPI

class AzureAPI(CloudAPI):
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        # Use the tenant_id, client_id, and client_secret to authenticate
        self.credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        self.subscription_client = SubscriptionClient(self.credential)
        self.access_token = self.credential.get_token('https://management.azure.com/.default').token

    def get_all_subscriptions(self):
        # https://azuresdkdocs.blob.core.windows.net/$web/python/azure-mgmt-resource/23.0.0/azure.mgmt.resource.subscriptions.html#module-azure.mgmt.resource.subscriptions
        subscription_iterator = self.subscription_client.subscriptions.list()
        subscriptions = list(subscription_iterator)
        return [subscription.subscription_id for subscription in subscriptions]

    def get_cost(self, subscription_id: str, start_date: datetime.datetime, end_date: datetime.datetime):
        # setup cost management client with the subscription id
        cost_management_client = CostManagementClient(self.credential)
        scope = f'/subscriptions/{subscription_id}/'
        # Convert the datetime objects to strings in the required format
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        print(f"Looking for data between {start_date_str} and {end_date_str}")
        while True:
            query = QueryDefinition(
                type='ActualCost',
                timeframe=f'{start_date_str}/{end_date_str}',
                dataset = QueryDataset(
                    granularity="daily",
                    grouping=[ { 'type': 'Dimension', 'name': 'ResourceId' }, { 'type': 'Dimension', 'name': 'ChargeType' } ],
                )
            )
            try:
                result = cost_management_client.query.usage(scope, query)
            except ResourceNotFoundError:
                print(f"Subscription has incorrect type (like Azure Sponsorship for example), which doesn't allow use of cost management API.")
                raise
            except HttpResponseError as e:
                time.sleep(5)
                continue
            break

        if len(result.rows) > 0:
            # Get the column names
            column_names = [column.name for column in result.columns]
            # Create a list of dictionaries
            data = [dict(zip(column_names, row)) for row in result.rows]
            return data
        else:
            print("Result retreived successfully, but it contains no data. It might be a very new subscription.")
            return None
