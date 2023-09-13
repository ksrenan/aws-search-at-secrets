#!/usr/bin/env python3
import boto3
import argparse
import json
import inquirer

def searchAtSecrets(string, profile):
    session = boto3.Session(profile_name=profile)
    client = session.client('secretsmanager')
    p = client.get_paginator('list_secrets')
    paginator = p.paginate().build_full_result()
    secrets = []
    for page in paginator['SecretList']:
        response = client.get_secret_value(SecretId=page['Name'])
        value = response['SecretString']
        if string.lower() in value.lower():
            secrets.append(page['Name'])
    if secrets:
        return f"Secrets found with string '{stringToSearch}':\n" + json.dumps(secrets, indent=2)
    else:
        return "String not found in the secrets of this account"
    
def get_account_id(profile):
    session = boto3.Session(profile_name=profile)
    client = session.client('sts')
    return client.get_caller_identity()["Account"]
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "Search string at all your AWS Secrets Manager service")
    parser.add_argument("-s", "--string", dest="string", required=True, help="String to search at Secrets")
    options = parser.parse_args()
    stringToSearch = options.string

    available_profiles = boto3.session.Session().available_profiles

    questions = [
    inquirer.List('profile_chosen',
                    message="Com qual perfil você deseja executar esse comando? Use as setas do teclado para selecionar. Seleção atual",
                    choices=available_profiles,
                ),
    ]
    answer_profile = inquirer.prompt(questions)

    profile = answer_profile["profile_chosen"]
    account_id = get_account_id(profile)

    print(f"String to search: {stringToSearch} | AWS profile: {profile} | AWS Account: {account_id}")
    print(f"Searching string '{stringToSearch}' at AWS Secrets Manager for account: {profile} -> {account_id} ...")

    try:
        print(searchAtSecrets(stringToSearch, profile))
    except:
        print("[ERROR] Something went wrong, please check if you filled out correctly or if your profiles are correctly set up on your computer.")

print("Finished")