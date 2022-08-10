import ast


event = {'name': '900075289847431794ca4d99a76d74ed', 'mode': 'live', 'queryParams': '{token=Wp8LJkWNh3}'}

query_param = event['queryParams'].split('=')
token = query_param[1].replace('}', '')
print(token)