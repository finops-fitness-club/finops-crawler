# finops-crawler for OpenAI

[Main documentation](/) about the idea, structure and contribution. It's a package for getting Azure cost data into Python. The group-by dimensions are ResourceId and ChargeType to provide maximum meaningful granularity.

## Setup

OpenAI has an API ([documentation](https://platform.openai.com/docs/api-reference/authentication)), but it doesn't contain much about looking at usage over time. It specifies that some API calls incur usage tokens, but only for that single API call.

The approach taken in this package is an undocumented one and may break at any time. It uses an API that the OpenAI website uses to show billing data. Someone (*bhavish.pahwa*) found it and posted about it on [OpenAI forums](https://community.openai.com/t/how-can-i-check-openai-usage-with-python/117418/10). We've just packaged it into a Python function.

Nevertheless, it requires one piece of setup, which is creating the API key itself. Go to the [OpenAI platform API keys page](https://platform.openai.com/account/api-keys) and set up an API key. To be precise, then without already having an API key, all the costs will be zero as the paid account only incurs usage costs for API usage in the first place.

Another piece of information needed is an organization ID, which can be found on the [Settings page](https://platform.openai.com/account/org-settings).

Put those two values into environment variables:
```env
OPENAI_ORG_ID=your_org_id_from_settings_page
OPENAI_API_KEY=your_api_key
```

## Usage

Copy-paste the following code into a Python file and run it (also found in the [example.py](example.py) file).
```python
# nothing to copy here at the moment, the code doesn't work due to changes in the API
```

A successful run results in a list of dicts with the fields `timestamp`, `date` (added by the package), and `line_items` (which is itself a list of dicts with model names and costs).


Enjoy :)

Email: finops.fitness.club@gmail.com
