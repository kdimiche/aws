import config

import argparse
import ConfigParser

import boto
from boto import sts
import os


def get_aws_cli_config_file_path(
    aws_cli_config_file='config',
    home_path=os.path.expanduser('~'),
):

    aws_cli_config_file_path = os.path.join(home_path, '.aws', aws_cli_config_file)
    return aws_cli_config_file_path


def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument(
        '-u', '--aws_username',
        type=str,
        required=True,
        help='AWS IAM Username.',
    )

    parser.add_argument(
        '-m', '--mfa_token',
        type=str,
        required=True,
        help='AWS MFA Token code.',
    )

    parser.add_argument(
        '-e', '--environment',
        type=str,
        choices=['dev', 'prd'],
        default='dev',
        help='Environment.  Used to associate with AWS account.',
    )

    # Parse Commandline Arguments
    args = parser.parse_args()
    mfa_token = args.mfa_token
    environment = args.environment
    aws_username = args.aws_username

    # Get AWS account_id from account name
    aws_account_id = config.AWS_ACCOUNTS[environment]

    # Assemble AWS MFA serial number
    mfa_serial_number = 'arn:aws:iam::{}:mfa/{}'.format(aws_account_id, aws_username)

    # Assemble profile names
    profile_name = 'profile {}'.format(environment)
    profile_init = 'profile init_{}'.format(environment)

    # Get AWS CLI config path
    aws_cli_config_file_path = get_aws_cli_config_file_path()

    # get AWS credentials from init profiles
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(aws_cli_config_file_path)

    # Get the init profile's access key and secret key
    if not configuration.has_section(profile_init):
        raise NameError('"[{}]" is not in the AWS CLI config file "{}"'.format(
            profile_init, aws_cli_config_file_path))

    aws_access_key_id = configuration.get(profile_init, 'aws_access_key_id')
    aws_secret_access_key = configuration.get(profile_init, 'aws_secret_access_key')

    # Create STS boto connection
    sts = boto.sts.STSConnection(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # Get session token
    session_token = sts.get_session_token(
        mfa_serial_number=mfa_serial_number,
        mfa_token=mfa_token)

    # Write Session token to AWS CLI Config file
    # Check if profile already exists. If not, add section

    if not configuration.has_section(profile_name):
        configuration.add_section(profile_name)

    # Set values to write
    configuration.set(profile_name, '# {} expiration'.format(profile_name), session_token.expiration)
    configuration.set(profile_name, 'aws_access_key_id', session_token.access_key)
    configuration.set(profile_name, 'aws_secret_access_key', session_token.secret_key)
    configuration.set(profile_name, 'aws_session_token', session_token.session_token)

    # Write values to file
    with open(aws_cli_config_file_path, 'wb') as configfile:
        configuration.write(configfile)


if __name__ == '__main__':
    main()