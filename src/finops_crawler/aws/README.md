# finops-crawler for AWS

[Main documentation](/) about the idea, structure and contribution. It's a package for getting Azure cost data into Python. The group-by dimensions are ResourceId and ChargeType to provide maximum meaningful granularity.

## Setting up the service principal and permissions

### Quickstart

Using [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html). It creates a user, an access key for the user, a custom IAM policy, and then attaches the policy to the user.

Step 0, enable AWS Cost Explorer, then wait 24 hours. More in the [official documentation](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-enable.html).

Step 1, create a user:
```bash
aws iam create-user --user-name finops_crawler
```
outputs:
```json
{
    "User": {
        "Path": "/",
        "UserName": "finops_crawler",
        "UserId": "USER_ID_THAT_WAS_JUST_CREATED",
        "Arn": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:user/finops_crawler",
        "CreateDate": "2023-06-29T15:28:32+00:00"
    }
}
```
Step 2, create access key:
```bash
aws iam create-access-key --user-name finops_crawler
```
outputs:
```json
{
    "AccessKey": {
        "UserName": "finops_crawler",
        "AccessKeyId": "YOUR_ACCESS_KEY_ID",
        "Status": "Active",
        "SecretAccessKey": "YOUR_SECRET_ACCESS_KEY",
        "CreateDate": "2023-06-29T15:28:50+00:00"
    }
}
```
Step 3, create a custom policy:
```bash
aws iam create-policy --policy-name FinopsCrawlerCustomPolicy --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "FinopsCrawlerCustomPolicy",
            "Effect": "Allow",
            "Action": [
                "organizations:DescribeAccount",
                "organizations:ListAccounts",
                "ce:*"
            ],
            "Resource": "*"
        }
    ]
}'
```

Step 4, attach the policy to the user:
```bash
aws iam attach-user-policy --user-name finops_crawler --policy-arn arn:aws:iam::YOUR_AWS_ACCOUNT_ID:policy/FinopsCrawlerCustomPolicy
```

Then set environment variables:
```env
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
```


## Long version

The package reads cost and usage data from a single AWS account or all AWS Organization accounts (untested yet).

The service that allows doing it in AWS is called Cost Explorer and it's not enabled by default. It has to be enabled by the root account or management account in the case of organizations. Please follow the [official documentation](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-enable.html). It might take up to 24 hours for it to be available in the UI and API.

### Step 1 - Create the user

The easiest way to have this script authorized to AWS is by creating a separate user and giving it the minimum amount of permissions required.  We suggest giving it a descriptive name, like "finops_crawler".

User creation gives you the user ID, but it's used in this flow. It also displays your Tenant ID, which you can also find elsewhere (upper corner of the AWS UI).

```bash
aws iam create-user --user-name finops_crawler
```

If you do it via the CLI then the result looks like this:
```json
{
    "User": {
        "Path": "/",
        "UserName": "finops_crawler",
        "UserId": "USER_ID_THAT_WAS_JUST_CREATED",
        "Arn": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:user/finops_crawler",
        "CreateDate": "2023-06-29T15:28:32+00:00"
    }
}
```


### Step 2 - Create an access key for the user

Users, by default, are created as users of the web interface. Adding programmatic access capabilities is a separate command, which we will do next.

```bash
aws iam create-access-key --user-name finops_crawler
```
outputs:
```json
{
    "AccessKey": {
        "UserName": "finops_crawler",
        "AccessKeyId": "YOUR_ACCESS_KEY_ID",
        "Status": "Active",
        "SecretAccessKey": "YOUR_SECRET_ACCESS_KEY",
        "CreateDate": "2023-06-29T15:28:50+00:00"
    }
}
```

### Step 3 - Create a custom policy for permissions

AWS has some preset policy bundles as well, but the closest one is extremely wide (too many permissions) and that's why we suggest creating a custom policy instead. Once again, we suggest using a descriptive name.

It will remain there in AWS and is not user-specific. In the next step, we will attach it to the user we created in the first step.

```bash
aws iam create-policy --policy-name FinopsCrawlerCustomPolicy --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "FinopsCrawlerCustomPolicy",
            "Effect": "Allow",
            "Action": [
                "organizations:DescribeAccount",
                "organizations:ListAccounts",
                "ce:*"
            ],
            "Resource": "*"
        }
    ]
}'
```

It might be that only a subset of the `ce` permission domain is sufficient, but it needs additional testing.

The `organizations` permission domain is used in a forward-looking manner as we plan to extend the functionality also to accounts that are part of an AWS Organization.

### Step 4 - Attach the custom policy to the user

Lastly, we need to put the pieces together by attaching the custom policy to the user. As long as it's there then the user will be able to access the Cost Explorer data.

```bash
aws iam attach-user-policy --user-name finops_crawler --policy-arn arn:aws:iam::YOUR_AWS_ACCOUNT_ID:policy/FinopsCrawlerCustomPolicy
```

To remove the permission you can do any of the three things: a) delete the user, b) de-attach the policy from the user, or c) delete the policy itself.


### Step 5 - Environment variables for the script

One should never write credentials directly into code. Thus, there is a way to read it from the environment variables at runtime. This is also how this script expects the credentials.

This is what should exist in your environment variables before running the script. Note that the values come from the output of the second step.

```env
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
```

### Step 6 - Use the package

Copy-paste the following code into a Python file and run it (also found in the [example.py](example.py) file).
```python
import datetime
from finops_crawler import aws, credentials_provider

credentials = credentials_provider.api()
aws_costs_client = aws.costs_api(*credentials.get_credentials('aws'))

today = datetime.datetime.now().date()
seven_days_ago = today - datetime.timedelta(days=7)

cost_data = aws_costs_client.get_cost(seven_days_ago, today)

print(cost_data)
```

A successful run results in a list of dicts with the format as described under the [ResultsByTime](https://docs.aws.amazon.com/cli/latest/reference/ce/get-cost-and-usage.html#output) part of the output.

Enjoy :)

Email: finops.fitness.club@gmail.com
