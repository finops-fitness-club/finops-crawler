import datetime
from common import credentials_provider
from finops_crawler import aws

credentials = credentials_provider()

aws_access_key_id, aws_secret_access_key = credentials.get_credentials('aws')
aws_costs_client = aws.costs_api(aws_access_key_id, aws_secret_access_key)

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

cost_data = aws_costs_client.get_cost(seven_days_ago, today)

print(cost_data)
