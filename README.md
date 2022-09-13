# Welcome to your CDK TypeScript project

This is an automation project using CDK development with TypeScript.

## Purpose

Setup Service Catalog Portfolio, Product for provisioning **Inspection VPC** with **AWS Network Firewall** in *Shared Network Account*.

- Creates Service Catalog Portfolio
- Creates Service Catalog Product

## Setup

- Access to this Service Catalog Portfolio is granted to *IAM User Group*: **sc-inspectvpcnfw-endusers**
- By default `scenduser` IAM user is added to **sc-inspectvpcnfw-endusers** *IAM User Group*

> To change default IAM user `scenduser`, CDK app needs to be redeployed
> - Change the IAM user name in `cdk.json`

> Default S3 Bucket: `sh-network-dev-bucket1`

### Upload files

- src\inspectionvpc_nfw_provider.yaml to S3 Bucket
- src\calc_cidr.zip to S3 Bucket
- src\retrieve_vpceids.zip to S3 Bucket

## Provisioning Service Catalog Product

- Login to *Shared Network Account* as **scenduser**
- Select **Inspection VPC NFW** from *Products* page
- Launch Product from *Service Catalog Console*
- Provide Parameter:
  - **TransitGatewayId** from *Shared Network Account*

### Result

- Inspection VPC is created
- 6 Subnets are created in 2 Availability Zones (3 subnets in each AZ)
- 1 Route Table per each Subnet is created
- AWS Network Firewall is created
- AWS Network Firewall Policy is created
  - Policy is empty by default (*No Rule Groups are associated with Policy*)
- Route to Firewall VPC Endpoints is added to Firewall Subnets
- Transit Gateway Attachment is created for Inspection VPC

## Deprovisioning Service Catalog Product

- Login to *Shared Network Account* as **scenduser**
- Select the previously provisioned product for **Inspection VPC NFW**
- Select *Actions* -> *Terminate*

### Result

- Transit Gateway Attachment is deleted
- AWS Network Firewall is deleted
  - Firewall Policy is deleted
- Inspection VPC is deleted

## Useful commands

* `npm install`     downloads node module dependencies
* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template
