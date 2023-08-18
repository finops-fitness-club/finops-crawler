import datetime
from finops_crawler import aws, credentials_provider

credentials = credentials_provider.api()
aws_costs_client = aws.costs_api(*credentials.get_credentials('aws'))

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

cost_data = aws_costs_client.get_cost(seven_days_ago, today)

print(cost_data)
