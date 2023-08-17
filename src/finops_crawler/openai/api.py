import requests
import datetime
import os
from typing import Optional, Union
from finops_crawler.base import CloudAPI

class OpenAIAPI(CloudAPI):
    def __init__(self, openai_org_id: Optional[str] = None, openai_api_key: Optional[str] = None):
        """
            Initialize OpenAIApi instance with OpenAI organization ID and API key.

            Retrieves the OpenAI organization ID and API key from parameters or environment variables if not provided.

            Args:
                openai_org_id (str, optional): OpenAI organization ID. If not provided, the function attempts to get the value from an environment variable named 'OPENAI_ORG_ID'.
                openai_api_key (str, optional): OpenAI API key. If not provided, the function attempts to get the value from an environment variable named 'OPENAI_API_KEY'.

            Raises:
                ValueError: If neither the parameters nor the corresponding environment variables are set.
            
            Note:
                API documentation: https://platform.openai.com/docs/api-reference/authentication
        """
        if openai_org_id is None:
            openai_org_id = os.getenv('OPENAI_ORG_ID')
        if not openai_org_id:
            raise ValueError('OPENAI_ORG_ID not set')

        if openai_api_key is None:
            openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError('OPENAI_API_KEY not set')

        self.base_url = 'https://api.openai.com/v1'
        self.headers = {'Authorization': f'Bearer {openai_api_key}', 'OpenAI-Organization': openai_org_id}


    def get_cost(self, start_date: Union[str, datetime.datetime], end_date: Union[str, datetime.datetime]):
        """
        no longer works. Using it outside of a browser session has been disabled by OpenAI
        """
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        results_by_time = []

        url = f'{self.base_url}/dashboard/billing/usage?start_date={start_date_str}&end_date={end_date_str}'

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(response.reason)
            raise Exception(f'GET /billing/usage failed with status code {response.status_code}.')

        results_by_time = response.json()['daily_costs']

        for item in results_by_time:
            item_date = datetime.datetime.fromtimestamp(item["timestamp"]).strftime('%Y-%m-%d')
            item["date"] = item_date

        return results_by_time
