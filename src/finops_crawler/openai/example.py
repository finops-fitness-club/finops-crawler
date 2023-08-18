import datetime
from finops_crawler import openai, credentials_provider

credentials = credentials_provider.api()

openai_costs_client = openai.api(*credentials.get_credentials('openai'))

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

# cost_data = openai_costs_client.get_cost(seven_days_ago, today)

# print(cost_data)
