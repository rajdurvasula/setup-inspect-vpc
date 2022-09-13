import os
import sys
import json
import boto3
import urllib3

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

def send_default_response(event, context):
    send_response(event, context, 'SUCCESS', responseData)

def lambda_handler(event, context):
    print(f"REQUEST RECEIVED: {json.dumps(event, default=str)}")
    responseData = {}
    resProps = event['ResourceProperties']
    az1 = resProps['Az1']
    az2 = resProps['Az2']
    firewallArn = resProps['FwArn']
    try:
        if 'RequestType' in event:
            if event['RequestType'] == 'Create':
                nfw_client = session.client('network-firewall')
                response = nfw_client.describe_firewall(FirewallArn=firewallArn)
                vpceId1 = response['FirewallStatus']['SyncStates'][az1]['Attachment']['EndpointId']
                vpceId2 = response['FirewallStatus']['SyncStates'][az2]['Attachment']['EndpointId']
                responseData = {
                    'FwVpceId1': vpceId1,
                    'FwVpceId2': vpceId2
                }
                print('Returning Response: ')
                print(json.dumps(responseData))
                send_response(event, context, 'SUCCESS', responseData)
            else:
                send_default_response(event, context)
    except Exception as e:
        print(f'failed in describe_firewall(..): {e}')
        print(str(e))
        send_response(event, context, 'SUCCESS', responseData)