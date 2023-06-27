import datetime
import boto3
from typing import Optional, Union
from botocore.exceptions import BotoCoreError
from finops_crawler.base import CloudAPI

class AWSAPI(CloudAPI):
    def __init__(self, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None):
        """
        Initialize AWSAPI.

        Args:
            aws_access_key_id (str, optional): AWS Access Key ID. If not provided, boto3 will 
                fall back to the credentials stored in your environment.
            aws_secret_access_key (str, optional): AWS Secret Access Key. If not provided, boto3 
                will fall back to the credentials stored in your environment.
        """
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def get_account_info(self):
        """
        Retrieves the AWS account number for the current user.

        This function uses the AWS Security Token Service (STS) GetCallerIdentity
        operation, which returns details about the IAM user or role whose 
        credentials are used to call the operation.

        Returns:
            str: AWS account number of the current user.

        Note:
            More information about the AWS STS GetCallerIdentity operation can be 
            found in the AWS documentation: 
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.get_caller_identity
        """
        client = self.session.client('sts') 
        identity = client.get_caller_identity()
        return identity['Account']

    def get_all_accounts(self):
        """
        Retrieves a list of all AWS account IDs in the organization.

        This function uses the AWS Organizations ListAccounts operation, which
        returns a list of all the accounts in the organization. If the AWS account
        is not part of any organization, the function will return False.

        Returns:
            list: A list of AWS account IDs in the organization. If the AWS account is 
            not part of any organization, returns False.

        Raises:
            botocore.exceptions.BotoCoreError: If there's an issue when making the request to AWS.

        Note:
            More information about the AWS Organizations ListAccounts operation can be found in the 
            AWS documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_accounts
        """
        client = self.session.client('organizations') 
        paginator = client.get_paginator('list_accounts')
        accounts = []
        try:
            for page in paginator.paginate():
                for account in page['Accounts']:
                    accounts.append(account['Id'])
                    print(account['Id'])
        except client.exceptions.AWSOrganizationsNotInUseException as e:
            print("Your account is not a member of an organization.")
            return False

        except BotoCoreError as e:
            print(f"Unexpected AWS error: {e}")

        return accounts

    def get_cost(self, start_date: Union[str, datetime.datetime], end_date: Union[str, datetime.datetime]):
        """
        Retrieves the cost of AWS services used over a specified time period.

        This function calls the AWS Cost Explorer GetCostAndUsage operation, which
        provides metrics associated with your AWS costs, split by service and usage type.
        Costs are presented on a daily basis.

        Args:
            start_date (datetime.datetime): The start date for retrieving AWS cost data.
                Data is returned for a time period that begins at the start date and
                ends at the end date.
            end_date (datetime.datetime): The end date for retrieving AWS cost data.
                Data is returned for a time period that begins at the start date and
                ends at the end date.

        Returns:
            list: A list of results by time. Each result includes the time period and metrics
            associated with the AWS costs, grouped by service and usage type.

        Raises:
            botocore.exceptions.BotoCoreError: If there's an issue when making the request to AWS.
            botocore.exceptions.ClientError: If there's a client-side error with boto3.

        Note:
            More information about the AWS Cost Explorer GetCostAndUsage operation can be found in the 
            AWS documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_cost_and_usage
        """
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        results_by_time = []

        client = self.session.client('ce')

        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date_str,
                'End': end_date_str
            },
            Granularity='DAILY',
            Metrics=[
                'UnblendedCost',
            ],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'},
            ],
        )
        results_by_time += response['ResultsByTime']
        if 'NextPageToken' in response:
            next_page_token = response['NextPageToken']
            while True:
                response = client.get_cost_and_usage(
                    TimePeriod={
                        'Start': start_date_str,
                        'End': end_date_str
                    },
                    Granularity='DAILY',
                    Metrics=[
                        'UnblendedCost',
                    ],
                    GroupBy=[
                        {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                        {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'},
                    ],
                    NextPageToken = next_page_token
                )
                results_by_time += response['ResultsByTime']
                if 'NextPageToken' in response:
                    next_page_token = response['NextPageToken']
                else:
                    break

        return results_by_time
