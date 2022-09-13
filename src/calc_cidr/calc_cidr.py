import os
import sys
import json
import boto3
from ipaddress import IPv4Network, ip_network
import urllib3

SUBNET_CIDR_NETMASK = int(24)
session = boto3.Session()
responseData = {}

def send_response(event, context, responseStatus, responseData, physicalResourceId=None,noEcho=False):
    responseUrl = event['ResponseURL']
    ls = context.log_stream_name
    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'View details in Log Stream: '+ls
    responseBody['PhysicalResourceId'] = physicalResourceId or ls
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData
    jsonResponseBody = json.dumps(responseBody)
    print('ResponseBody: \n'+jsonResponseBody)
    headers = {
        'content-type': '',
        'content-length': str(len(jsonResponseBody))
    }
    http = urllib3.PoolManager()
    try:
        response = http.request('PUT', responseUrl, body=jsonResponseBody, headers=headers)
        print('StatusCode = '+response.reason)
    except Exception as e:
        print(f'send_response(..) failed executing requests.put(..): {e}')

def get_cidr(vpc_id):
    try:
        ec2_client = session.client('ec2')
        response = ec2_client.describe_vpcs(VpcIds=[ vpc_id ])
        vpc = response['Vpcs'][0]
        vpc_cidr_block = vpc['CidrBlock']
        print('Return Vpc Id: {}'.format(vpc_cidr_block))
        return vpc_cidr_block
    except Exception as e:
        print(f'failed in describe_vpcs(..): {e}')
        print(str(e))

def get_subnet_cidrs(vpc_cidr_block, count):
    try:
        subnet_cidrs = list(ip_network(vpc_cidr_block).subnets(new_prefix=SUBNET_CIDR_NETMASK))[0:count]
        return subnet_cidrs
    except Exception as e:
        print(f'failed in get_subnet_cidr: {e}')
        print(str(e))

def send_default_response(event, context):
    send_response(event, context, 'SUCCESS', responseData)

def lambda_handler(event, context):
    print(f"REQUEST RECEIVED: {json.dumps(event, default=str)}")
    resProps = event['ResourceProperties']
    vpc_id = resProps['vpc_id']
    try:
        if 'RequestType' in event:
            if event['RequestType'] == 'Create':
                vpc_cidr_block = get_cidr(vpc_id)
                subnet_cidrs = get_subnet_cidrs(vpc_cidr_block, 6)
                subnet_cidr_strs = []
                for subnet_cidr in subnet_cidrs:
                    subnet_cidr_strs.append(str(IPv4Network(subnet_cidr)))
                responseData = {
                    'vpc_cidr': vpc_cidr_block,
                    'pub_subnet_1': subnet_cidr_strs[0],
                    'pub_subnet_2': subnet_cidr_strs[1],
                    'tgw_subnet_1': subnet_cidr_strs[2],
                    'tgw_subnet_2': subnet_cidr_strs[3],
                    'fw_subnet_1': subnet_cidr_strs[4],
                    'fw_subnet_2': subnet_cidr_strs[5]
                }
                print('Returning Response: ')
                print(json.dumps(responseData))
                send_response(event, context, 'SUCCESS', responseData)
            else:
                # handle any other RequestType
                send_default_response(event, context)
    except Exception as e:
        print(f'failed in lambda_handler: {e}')
        print(str(e))
        send_response(event, context, 'FAILED', responseData)