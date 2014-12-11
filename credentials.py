import config
import ConfigParser

import os


def get_aws_cli_config_file_path(
    aws_cli_config_file='config',
    home_path=os.path.expanduser('~'),
):

    aws_cli_config_file_path = os.path.join(home_path, '.aws', aws_cli_config_file)
    return aws_cli_config_file_path


def get_credentials(
        environment,
):
    # Get AWS account_id from account name
    aws_account_id = config.AWS_ACCOUNTS[environment]

    # Assemble profile name
    profile_name = 'profile {}'.format(environment)

    # Get AWS CLI config path
    aws_cli_config_file_path = get_aws_cli_config_file_path()

    # get AWS credentials from init profiles
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(aws_cli_config_file_path)

    aws_access_key_id = configuration.get(profile_name, 'aws_access_key_id')
    aws_secret_access_key = configuration.get(profile_name, 'aws_secret_access_key')
    aws_session_token = configuration.get(profile_name, 'aws_session_token')

    return aws_access_key_id, aws_secret_access_key, aws_session_token
