import datetime
import time
import boto3
from finops_crawler.base import CloudAPI

class AWSAPI(CloudAPI):
    def __init__(self, aws_access_key_id:str=None, aws_secret_access_key:str=None):
        """
        Initialize AWSAPI.

        :param aws_access_key_id: AWS Access Key ID. If not provided, boto3 will fall back to the credentials stored in your environment.
        :param aws_secret_access_key: AWS Secret Access Key. If not provided, boto3 will fall back to the credentials stored in your environment.
        """
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def get_all_accounts(self):
        client = self.session.client('organizations') 
        paginator = client.get_paginator('list_accounts')
        accounts = []
        for page in paginator.paginate():
            for account in page['Accounts']:
                accounts.append(account['Id'])
                print(account['Id'])
        return accounts

