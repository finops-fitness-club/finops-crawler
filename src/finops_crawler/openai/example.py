import datetime
from common import credentials_provider
from finops_crawler import openai

credentials = credentials_provider()

org_id, api_key = credentials.get_credentials('openai')
openai_costs_client = openai.costs_api(org_id, api_key)

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

cost_data = openai_costs_client.get_cost(seven_days_ago, today)

print(cost_data)
