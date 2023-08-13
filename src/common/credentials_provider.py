import os
import yaml

class CredentialsProvider:

    def __init__(self, credentials_file = 'credentials_config.yml'):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(current_dir, credentials_file)

        with open(credentials_path, 'r') as f:
            try:
                self.config = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)

    def get_credentials(self, platform):
        creds = self.config.get(platform)
        if not creds:
            raise ValueError(f"No configuration found for {platform}")
        values = []
        errors = []
        for f in creds['fields']:
            value = os.getenv(f['key'])
            if not value:
                errors.append(f['key'])
                continue
            values.append(value)
        if len(errors) > 0:
            raise ValueError(f"Missing environment variable(s) for the following: {', '.join(errors)}")
        return tuple(values)
