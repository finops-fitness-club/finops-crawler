import os
import datetime
from finops_crawler import openai

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

org_id = os.getenv('OPENAI_ORG_ID')
api_key = os.getenv('OPENAI_API_KEY')
openai_costs_client = openai.costs_api(org_id, api_key)
cost_data = openai_costs_client.get_cost(seven_days_ago, today)

print(cost_data)
