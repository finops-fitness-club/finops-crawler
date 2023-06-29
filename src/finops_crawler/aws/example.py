import os
import datetime
from finops_crawler import aws

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_costs_client = aws.costs_api(aws_access_key_id, aws_secret_access_key)
cost_data = aws_costs_client.get_cost(seven_days_ago, today)

print(cost_data)
