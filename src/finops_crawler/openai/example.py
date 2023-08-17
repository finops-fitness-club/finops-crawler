import datetime
from common import credentials_provider
from finops_crawler import openai

credentials = credentials_provider()

openai_costs_client = openai.costs_api(*credentials.get_credentials('openai'))

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

cost_data = openai_costs_client.get_cost(seven_days_ago, today)

print(cost_data)
