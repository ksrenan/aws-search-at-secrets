# aws-search-at-AWS-Secrets-Manager
Search any string at all your secrets saved at AWS Secrets Manager with multi-account/SSO support.

## E.g.
You have 300 secrets saved in the AWS Secrets Manager at your aws account, and you want to see which ones have the string "host_xdb", then you can run the command: ````python3 searchAtSecrets.py -s host_xdb````

The script will analyze each of the secrets value and tell you if the string was found.

### Help to use:
```
python3 searchAtSecrets.py -h
```
Usage:
````
python3 searchAtSecrets.py -s [STRING]
````
The script will ask you which AWS profile you want to use to run.