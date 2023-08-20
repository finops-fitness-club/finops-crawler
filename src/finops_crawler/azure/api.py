import datetime
import time
import requests
import os
import csv
import io
from typing import Union
from finops_crawler.base import CloudAPI

class AzureAPI(CloudAPI):
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        # https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow#first-case-access-token-request-with-a-shared-secret
        if tenant_id is None:
            tenant_id = os.getenv('AZURE_TENANT_ID')
        if not tenant_id:
            raise ValueError('AZURE_TENANT_ID not set')

        if client_id is None:
            client_id = os.getenv('AZURE_CLIENT_ID')
        if not client_id:
            raise ValueError('AZURE_CLIENT_ID not set')

        if client_secret is None:
            client_secret = os.getenv('AZURE_CLIENT_SECRET')
        if not client_secret:
            raise ValueError('AZURE_CLIENT_SECRET not set')

        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

        payload = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'https://management.azure.com/.default'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response_json = response.json()

        access_token = response_json.get('access_token')

        self.headers = {'Authorization': f'Bearer {access_token}'}


    def get_all_subscriptions(self):
        # https://azuresdkdocs.blob.core.windows.net/$web/python/azure-mgmt-resource/23.0.0/azure.mgmt.resource.subscriptions.html#module-azure.mgmt.resource.subscriptions
        # make the POST request to the Cost Management API
        url = 'https://management.azure.com/subscriptions?api-version=2020-01-01'

        response = requests.get(url=url, headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            print(f"API returned error {response.status_code}: {response.reason}. Message: {response.json()['error']['message']}")
            raise

        result = response.json()['value']
        if len(result) == 0:
            print("Result retrieved successfully, but it contains no data.")
            raise ValueError("Empty result")

        subscriptions = [s['subscriptionId'] for s in result]
        return subscriptions


    def get_cost(self, subscription_id: str, start_date: Union[str, datetime.datetime], end_date: Union[str, datetime.datetime]):
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

        # build the body for the request
        body = {
            'type': 'ActualCost',
            'timeframe': 'Custom',
            'timePeriod': {
            'from': start_date_str,
            'to': end_date_str
            },
            'dataset': {
            'granularity': 'Daily',
            'aggregation': {
                'totalCost': {
                'name': 'Cost',
                'function': 'Sum'
                }
            },
            'grouping': [
                {'type': 'Dimension', 'name': 'ResourceId'},
                {'type': 'Dimension', 'name': 'ChargeType'}
            ]
            }
        }

        data = []

        # make the POST request to the Cost Management API
        url = f'https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.CostManagement/query?api-version=2019-11-01'
        response = requests.post(url=url, headers=self.headers, json=body)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            print(f"API returned error {response.status_code}: {response.reason}. Message: {response.json()['error']['message']}")
            raise

        result = response.json()['properties']
        if len(result['rows']) > 0:
            column_names = [column['name'] for column in result['columns']]
            rows = [dict(zip(column_names, row)) for row in result['rows']]
        else:
            print("Result retrieved successfully, but it contains no data. It might be a very new subscription.")
            raise ValueError("Empty result")

        data += rows

        # check if there's a nextLink field in the response
        if 'nextLink' in result:
            next_link = result['nextLink']

            # while there is a next link, get the next page of results
            while next_link:
                response = requests.post(next_link, headers=self.headers, json=body)
                if response.status_code == 429:
                    time.sleep(10)
                    continue
                result = response.json()['properties']
                if len(result['rows']) > 0:
                    column_names = [column['name'] for column in result['columns']]
                    rows = [dict(zip(column_names, row)) for row in result['rows']]
                else:
                    print("Result retrieved successfully, but it contains no data. It might be a very new subscription.")
                    raise ValueError("Empty result")

                # print(f"Results in this batch: {len(rows)}")
                data += rows

                # update the next_link value
                next_link = result.get('nextLink')
        # print(f"Total rows found: {len(data)}")


        if len(data) > 0:
            return data
        else:
            print("Result retreived successfully, but it contains no data. It might be a very new subscription.")
            return None

    def get_cost_detailed(self, subscription_id: str, start_date: Union[str, datetime.datetime], end_date: Union[str, datetime.datetime]):
        # info: https://learn.microsoft.com/en-us/azure/cost-management-billing/automate/automation-ingest-usage-details-overview
        # result: https://learn.microsoft.com/en-us/azure/cost-management-billing/automate/understand-usage-details-fields
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        # print(f"Looking for detailed cost data between {start_date_str} and {end_date_str}")

        body = {
            'metric': 'AmortizedCost',
            'timePeriod': {
                'start': start_date_str,
                'end': end_date_str
            }
        }

        data = []

        # scope here can be many different things, we're using subscriptions to keep the function parameters the same
        # https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-work-scopes#identify-the-resource-id-for-a-scope
        scope = f"subscriptions/{subscription_id}"
        # make the POST request to the Cost Management API
        url = f'https://management.azure.com/{scope}/providers/Microsoft.CostManagement/generateCostDetailsReport?api-version=2022-05-01'
        response = requests.post(url=url, headers=self.headers, json=body)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            print(f"API returned error {response.status_code}: {response.reason}. Message: {response.json()['error']['message']}")
            raise

        while response.status_code == 202:
            retry_after = int(response.headers.get('Retry-After', 5))
            url = response.headers.get('Location')
            if url is None:
                raise ValueError("Location for polling missing")
            # print(f"Sleeping for {retry_after} seconds before polling again")
            time.sleep(retry_after)
            response = requests.get(url=url, headers=self.headers)
            try:
                response.raise_for_status()
            except requests.HTTPError as e:
                print(f"API returned error {response.status_code}: {response.reason}. Message: {response.json()['error']['message']}")
                raise

        result = response.json()
        if result['status'] == 'Completed':
            manifest = result['manifest']
            # print(f"Result contains {manifest['blobCount']} blobs, looping through them")
            for i in range(manifest['blobCount']):
                # print(f"Downloading blob: {i}")
                blob_response = requests.get(url=manifest['blobs'][i]['blobLink'])
                csv_file_like_object = io.StringIO(blob_response.text)
                reader = csv.DictReader(csv_file_like_object)
                rows = list(reader)
                data += rows
                # print(f"Found {len(rows)} rows in blob {i}")
        else:
            print(f"Result retrieved successfully, but status is {result['status']} instead of Completed")
            raise ValueError("Empty result")

        # print(f"Total rows found: {len(data)}")

        if len(data) > 0:
            return data
        else:
            print("Result retreived successfully, but it contains no data. It might be a very new subscription.")
            return None
